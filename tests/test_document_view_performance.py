import time
import difflib
from pathlib import Path
from fastapi.testclient import TestClient

from versioning import api
from versioning.store import RevisionStore
from comments.store import CommentStore


def test_document_view_latest_only_is_fast(tmp_path: Path, monkeypatch):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    monkeypatch.setattr(api, "_store", rev_store)
    monkeypatch.setattr(api, "_comment_store", com_store)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    for i in range(100):
        rev_store.save_document("doc", f"line{i}", "u1")

    calls = {"count": 0}

    def slow_diff(*args, **kwargs):
        calls["count"] += 1
        time.sleep(0.001)
        return []

    monkeypatch.setattr(difflib, "unified_diff", slow_diff)
    client = TestClient(api.app)

    start = time.time()
    res = client.get("/docs/doc/view")
    latest_duration = time.time() - start
    assert res.status_code == 200
    assert calls["count"] == 1

    start = time.time()
    res = client.get("/docs/doc/view?latest_only=false")
    full_duration = time.time() - start
    assert res.status_code == 200
    assert calls["count"] == 101
    assert full_duration > latest_duration * 5
