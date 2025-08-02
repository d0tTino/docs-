from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from .store import RevisionStore
from comments.store import CommentStore
from .render import render_document
from agentauth import TokenStore

app = FastAPI()
_store = RevisionStore(Path("revision_store.json"))
_comment_store = CommentStore(Path("comments_store.json"))
_token_store = TokenStore(Path("api_tokens.json"))

_security = HTTPBearer()


def _get_agent(credentials: HTTPAuthorizationCredentials = Depends(_security)) -> str:
    agent_id = _token_store.verify(credentials.credentials)
    if agent_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return agent_id


def _notify_comments(doc_id: str, summary: str) -> None:
    """Placeholder notification workflow for document comments."""
    for c in _comment_store.list_comments(doc_id):
        # Real implementation could notify comment authors here
        print(f"Notify comment {c['comment_id']} on {doc_id}: {summary}")


class CommentCreate(BaseModel):
    section_ref: str
    author_id: str
    body: str


class CommentUpdate(BaseModel):
    body: Optional[str] = None
    status: Optional[str] = None


class DocUpdate(BaseModel):
    content: str
    author_id: str
    summary: str
    append: bool = True


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


@app.post("/docs/{doc_id}/comments")
def create_comment(doc_id: str, payload: CommentCreate):
    comment = _comment_store.add_comment(
        doc_id, payload.section_ref, payload.author_id, payload.body
    )
    return comment


@app.get("/docs/{doc_id}/comments")
def list_comments(doc_id: str):
    return _comment_store.list_comments(doc_id)


@app.patch("/comments/{comment_id}")
def update_comment(comment_id: int, payload: CommentUpdate):
    comment = _comment_store.update_comment(
        comment_id, body=payload.body, status=payload.status
    )
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@app.post("/tokens")
def create_token(payload: TokenCreate):
    token = _token_store.create_token(payload.agent_id)
    return token


@app.delete("/tokens/{token}")
def delete_token(token: str):
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
    new_content = current + payload.content if payload.append else payload.content
    revision = _store.save_document(doc_id, new_content, payload.author_id)
    _notify_comments(doc_id, payload.summary)
    return revision


@app.get("/docs/{doc_id}/render")
def render(doc_id: str):
    return render_document(doc_id, _store, _comment_store)
