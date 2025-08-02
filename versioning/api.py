from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .store import RevisionStore
from comments.store import CommentStore
from .render import render_document

app = FastAPI()
_store = RevisionStore(Path("revision_store.json"))
_comment_store = CommentStore(Path("comments_store.json"))


class CommentCreate(BaseModel):
    section_ref: str
    author_id: str
    body: str


class CommentUpdate(BaseModel):
    body: Optional[str] = None
    status: Optional[str] = None


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


@app.get("/docs/{doc_id}/render")
def render(doc_id: str):
    return render_document(doc_id, _store, _comment_store)
