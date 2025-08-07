from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import logging
import difflib
import time
import smtplib
from email.message import EmailMessage

import requests

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .store import RevisionStore
from comments.store import Comment, CommentStore
from .render import render_document
from agentauth import TokenStore
from notifications import SubscriptionStore
from ume.events import EventPayload, post_event

app = FastAPI()
_store = RevisionStore(Path("revision_store.sqlite"))
_comment_store = CommentStore(Path("comments_store.sqlite"))
_token_store = TokenStore(Path("api_tokens.json"))
_subscription_store = SubscriptionStore(Path("subscriptions_store.sqlite"))

_security = HTTPBearer()


def _get_agent(credentials: HTTPAuthorizationCredentials = Depends(_security)) -> str:
    agent_id = _token_store.verify(credentials.credentials)
    if agent_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return agent_id


def _notify_comments(doc_id: str, summary: str) -> None:
    """Notify authors of comments on ``doc_id`` about a new revision."""
    for c in _comment_store.list_comments(doc_id):
        payload = {
            "document_id": doc_id,
            "event_type": "revision_created",
            "summary": summary,
            "comment_id": c.comment_id,
        }
        _send_notification(c.author_id, "email", payload)


def _send_notification(subscriber_id: str, channel: str, payload: dict) -> None:
    """Dispatch notifications via supported channels with retries."""
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            if channel == "email":
                msg = EmailMessage()
                msg["Subject"] = f"{payload['event_type']} for {payload['document_id']}"
                msg["From"] = "noreply@example.com"
                msg["To"] = f"{subscriber_id}@example.com"
                msg.set_content(str(payload))
                with smtplib.SMTP("localhost") as smtp:
                    smtp.send_message(msg)
            else:
                url = f"http://{subscriber_id}.invalid/{channel}"
                response = requests.post(
                    url,
                    json={"subscriber_id": subscriber_id, **payload},
                    timeout=3,
                )
                response.raise_for_status()
            return
        except Exception as exc:  # pragma: no cover - logging is the focus
            logging.error("Notification attempt %s failed: %s", attempt, exc)
            if attempt == attempts:
                logging.error(
                    "Giving up on notifying %s via %s", subscriber_id, channel
                )
            else:
                time.sleep(min(0.5 * 2 ** (attempt - 1), 5))


def _notify_subscribers(
    doc_id: str,
    event_type: str,
    revision_id: Optional[int] = None,
    comment_id: Optional[int] = None,
) -> None:
    """Send notifications to all subscribers of ``doc_id``."""
    link = f"/docs/{doc_id}/comments/{comment_id}" if comment_id else None
    payload = {
        "document_id": doc_id,
        "event_type": event_type,
        "revision_id": revision_id,
    }
    if link:
        payload["comment_link"] = link
    for sub in _subscription_store.get_subscribers(doc_id):
        for channel in sub["channels"]:
            _send_notification(sub["subscriber_id"], channel, payload)


def _find_conflicts(
    base: str, incoming: str, current: str
) -> List[Dict[str, List[int]]]:
    """Return ranges of lines that conflict between ``incoming`` and ``current``.

    Ranges are expressed as lists of ``[start, end]`` indices for the base,
    incoming, and current contents so clients can present inline merge UI.
    """
    base_lines = base.splitlines()
    inc_lines = incoming.splitlines()
    cur_lines = current.splitlines()
    ours = [
        op
        for op in difflib.SequenceMatcher(None, base_lines, inc_lines).get_opcodes()
        if op[0] != "equal"
    ]
    theirs = [
        op
        for op in difflib.SequenceMatcher(None, base_lines, cur_lines).get_opcodes()
        if op[0] != "equal"
    ]
    conflicts: List[Dict[str, List[int]]] = []
    i = j = 0
    while i < len(ours) and j < len(theirs):
        _, oi1, oi2, oj1, oj2 = ours[i]
        _, ti1, ti2, tj1, tj2 = theirs[j]
        start = max(oi1, ti1)
        end = min(oi2, ti2)
        if start < end and inc_lines[oj1:oj2] != cur_lines[tj1:tj2]:
            conflicts.append(
                {
                    "base": [start, end],
                    "incoming": [oj1, oj2],
                    "current": [tj1, tj2],
                }
            )
        if oi2 <= ti2:
            i += 1
        if ti2 <= oi2:
            j += 1
    return conflicts


class CommentCreate(BaseModel):
    section_ref: str
    author_id: str
    body: str
    correlation_id: Optional[str] = None


class CommentUpdate(BaseModel):
    body: Optional[str] = None
    status: Optional[str] = None


class DocUpdate(BaseModel):
    content: str
    author_id: str
    summary: str
    append: bool = True
    base_version: Optional[int] = None
    correlation_id: Optional[str] = None


class DocResolve(BaseModel):
    content: str
    author_id: str
    summary: str
    base_version: int
    correlation_id: Optional[str] = None


class SubscriptionUpdate(BaseModel):
    subscriber_id: str
    channels: List[str]


class TokenCreate(BaseModel):
    agent_id: str


@app.get("/docs/{doc_id}/revisions")
def list_revisions(doc_id: str):
    return _store.list_revisions(doc_id)


@app.get("/docs/{doc_id}/revisions/{version}")
def get_revision(doc_id: str, version: int):
    revision = _store.get_revision(doc_id, version)
    if revision is None:
        raise HTTPException(status_code=404, detail="Revision not found")
    return revision


@app.get("/docs/{doc_id}/diff/{from_version}/{to_version}")
def diff_revisions(doc_id: str, from_version: int, to_version: int):
    try:
        diff = _store.diff_revisions(doc_id, from_version, to_version)
    except ValueError:
        raise HTTPException(status_code=404, detail="Revision not found")
    return {"diff": diff}


@app.get("/docs/{doc_id}/view")
def document_view(doc_id: str, latest_only: bool = True):
    """Return document content, comments and revision history with diffs.

    ``latest_only`` limits diff generation to just the most recent revision,
    avoiding expensive work when a document has many revisions.  Passing
    ``latest_only=false`` retains the original behaviour of producing diffs for
    every revision.
    """
    revisions = _store.list_revisions(doc_id)
    content = revisions[-1]["content"] if revisions else ""
    comments = _comment_store.list_comments(doc_id)

    if latest_only:
        history = [{**rev, "diff": ""} for rev in revisions]
        if revisions:
            prev = revisions[-2]["content"] if len(revisions) > 1 else ""
            last = revisions[-1]
            diff = "".join(
                difflib.unified_diff(
                    prev.splitlines(keepends=True),
                    last["content"].splitlines(keepends=True),
                    fromfile=f"v{last['version']-1}",
                    tofile=f"v{last['version']}",
                )
            )
            history[-1]["diff"] = diff
        return {"content": content, "comments": comments, "revisions": history}

    history = []
    previous = ""
    for rev in revisions:
        diff = "".join(
            difflib.unified_diff(
                previous.splitlines(keepends=True),
                rev["content"].splitlines(keepends=True),
                fromfile=f"v{rev['version']-1}",
                tofile=f"v{rev['version']}",
            )
        )
        history.append({**rev, "diff": diff})
        previous = rev["content"]
    return {"content": content, "comments": comments, "revisions": history}


@app.post("/docs/{doc_id}/comments")
def create_comment(
    doc_id: str, payload: CommentCreate, agent_id: str = Depends(_get_agent)
) -> Comment:
    if payload.author_id != agent_id:
        raise HTTPException(status_code=403, detail="author_id must match token")
    comment = _comment_store.add_comment(
        doc_id, payload.section_ref, payload.author_id, payload.body
    )
    revs = _store.list_revisions(doc_id)
    rev_id = revs[-1]["version"] if revs else None
    event = EventPayload(
        document_id=doc_id,
        event_type="comment_created",
        author_id=payload.author_id,
        timestamp=comment.created_at,
        revision_id=rev_id,
        correlation_id=payload.correlation_id,
    )
    post_event(event)
    _notify_subscribers(
        doc_id, "comment_created", revision_id=rev_id, comment_id=comment.comment_id
    )
    return comment


@app.get("/docs/{doc_id}/comments")
def list_comments(doc_id: str) -> List[Comment]:
    return _comment_store.list_comments(doc_id)


@app.patch("/comments/{comment_id}")
def update_comment(
    comment_id: int, payload: CommentUpdate, agent_id: str = Depends(_get_agent)
) -> Comment:
    existing = _comment_store.get_comment(comment_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing.author_id != agent_id:
        raise HTTPException(status_code=403, detail="author_id must match token")
    return _comment_store.update_comment(
        comment_id, body=payload.body, status=payload.status
    )


@app.post("/comments/{comment_id}/toggle")
def toggle_comment(comment_id: int, agent_id: str = Depends(_get_agent)) -> Comment:
    """Flip comment status between ``open`` and ``resolved``."""
    comment = _comment_store.get_comment(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != agent_id:
        raise HTTPException(status_code=403, detail="author_id must match token")
    new_status = "open" if comment.status == "resolved" else "resolved"
    return _comment_store.update_comment(comment_id, status=new_status)


@app.post("/docs/{doc_id}/subscriptions")
def upsert_subscription(
    doc_id: str, payload: SubscriptionUpdate, agent_id: str = Depends(_get_agent)
):
    _subscription_store.subscribe(doc_id, payload.subscriber_id, payload.channels)
    return {"status": "subscribed"}


@app.delete("/docs/{doc_id}/subscriptions/{subscriber_id}")
def delete_subscription(
    doc_id: str, subscriber_id: str, agent_id: str = Depends(_get_agent)
):
    _subscription_store.unsubscribe(doc_id, subscriber_id)
    return {"status": "unsubscribed"}


@app.post("/tokens")
def create_token(payload: TokenCreate, agent_id: str = Depends(_get_agent)):
    if payload.agent_id != agent_id:
        raise HTTPException(status_code=403, detail="agent_id must match token")
    token = _token_store.create_token(payload.agent_id)
    return token


@app.delete("/tokens/{token}")
def delete_token(token: str, agent_id: str = Depends(_get_agent)):
    token_agent = _token_store.verify(token)
    if token_agent != agent_id:
        raise HTTPException(status_code=403, detail="token does not belong to agent")
    _token_store.delete_token(token)
    return {"status": "deleted"}


@app.put("/docs/{doc_id}")
def update_document(
    doc_id: str, payload: DocUpdate, agent_id: str = Depends(_get_agent)
):
    if payload.author_id != agent_id:
        raise HTTPException(status_code=403, detail="author_id must match token")
    revs = _store.list_revisions(doc_id)
    current = revs[-1]["content"] if revs else ""
    latest_version = revs[-1]["version"] if revs else 0
    if payload.base_version is not None and payload.base_version != latest_version:
        try:
            diff = _store.diff_revisions(
                doc_id, payload.base_version, latest_version
            )
            base_rev = _store.get_revision(doc_id, payload.base_version)
            base_content = base_rev["content"] if base_rev else ""
            conflicts = _find_conflicts(base_content, payload.content, current)
        except ValueError:
            diff = ""
            conflicts = []
        raise HTTPException(
            status_code=409,
            detail={
                "diff": diff,
                "latest": latest_version,
                "conflicts": conflicts,
            },
        )
    new_content = current + payload.content if payload.append else payload.content
    try:
        revision = _store.save_document(
            doc_id, new_content, payload.author_id, latest_version
        )
    except ValueError:
        revs = _store.list_revisions(doc_id)
        latest_version = revs[-1]["version"] if revs else 0
        current = revs[-1]["content"] if revs else ""
        try:
            diff = _store.diff_revisions(
                doc_id, payload.base_version or latest_version, latest_version
            )
            base_rev = _store.get_revision(
                doc_id, payload.base_version or latest_version
            )
            base_content = base_rev["content"] if base_rev else ""
            conflicts = _find_conflicts(base_content, payload.content, current)
        except ValueError:
            diff = ""
            conflicts = []
        raise HTTPException(
            status_code=409,
            detail={"diff": diff, "latest": latest_version, "conflicts": conflicts},
        )
    event = EventPayload(
        document_id=doc_id,
        event_type="revision_created",
        author_id=payload.author_id,
        timestamp=revision.timestamp,
        revision_id=revision.version,
        correlation_id=payload.correlation_id,
    )
    post_event(event)
    _notify_subscribers(doc_id, "revision_created", revision_id=revision.version)
    _notify_comments(doc_id, payload.summary)
    return revision


@app.post("/docs/{doc_id}/resolve")
def resolve_document(
    doc_id: str, payload: DocResolve, agent_id: str = Depends(_get_agent)
):
    if payload.author_id != agent_id:
        raise HTTPException(status_code=403, detail="author_id must match token")
    revs = _store.list_revisions(doc_id)
    current = revs[-1]["content"] if revs else ""
    latest_version = revs[-1]["version"] if revs else 0
    if payload.base_version != latest_version:
        try:
            diff = _store.diff_revisions(
                doc_id, payload.base_version, latest_version
            )
            base_rev = _store.get_revision(doc_id, payload.base_version)
            base_content = base_rev["content"] if base_rev else ""
            conflicts = _find_conflicts(base_content, payload.content, current)
        except ValueError:
            diff = ""
            conflicts = []
        raise HTTPException(
            status_code=409,
            detail={
                "diff": diff,
                "latest": latest_version,
                "conflicts": conflicts,
            },
        )
    try:
        revision = _store.save_document(
            doc_id, payload.content, payload.author_id, latest_version
        )
    except ValueError:
        revs = _store.list_revisions(doc_id)
        latest_version = revs[-1]["version"] if revs else 0
        current = revs[-1]["content"] if revs else ""
        try:
            diff = _store.diff_revisions(
                doc_id, payload.base_version, latest_version
            )
            base_rev = _store.get_revision(doc_id, payload.base_version)
            base_content = base_rev["content"] if base_rev else ""
            conflicts = _find_conflicts(base_content, payload.content, current)
        except ValueError:
            diff = ""
            conflicts = []
        raise HTTPException(
            status_code=409,
            detail={"diff": diff, "latest": latest_version, "conflicts": conflicts},
        )
    event = EventPayload(
        document_id=doc_id,
        event_type="revision_created",
        author_id=payload.author_id,
        timestamp=revision.timestamp,
        revision_id=revision.version,
        correlation_id=payload.correlation_id,
    )
    post_event(event)
    _notify_subscribers(doc_id, "revision_created", revision_id=revision.version)
    _notify_comments(doc_id, payload.summary)
    return revision


@app.get("/docs/{doc_id}/render")
def render(doc_id: str):
    return render_document(doc_id, _store, _comment_store)
