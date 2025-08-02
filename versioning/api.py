from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException

from .store import RevisionStore

app = FastAPI()
_store = RevisionStore(Path("revision_store.json"))


@app.get("/docs/{doc_id}/revisions")
def list_revisions(doc_id: str):
    return _store.list_revisions(doc_id)


@app.get("/docs/{doc_id}/revisions/{version}")
def get_revision(doc_id: str, version: int):
    revision = _store.get_revision(doc_id, version)
    if revision is None:
        raise HTTPException(status_code=404, detail="Revision not found")
    return revision
