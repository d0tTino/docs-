from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from comments.store import CommentStore  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from versioning import api  # noqa: E402


def test_comment_store(tmp_path: Path):
    store = CommentStore(tmp_path / "db.sqlite")
    c1 = store.add_comment("doc1", "L1-2", "user1", "note")
    assert c1.comment_id == 1
    assert store.list_comments("doc1")[0]["body"] == "note"

    store.update_comment(1, status="resolved")
    assert store.get_comment(1)["status"] == "resolved"


def test_comment_endpoints(tmp_path: Path, monkeypatch):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    monkeypatch.setattr(api, "_store", rev_store)
    monkeypatch.setattr(api, "_comment_store", com_store)
    monkeypatch.setattr(api, "post_event", lambda e: None)
    client = TestClient(api.app)

    rev_store.save_document("doc1", "line1\nline2", "user1")
    res = client.post(
        "/docs/doc1/comments",
        json={"section_ref": "L1-1", "author_id": "user1", "body": "test"},
    )
    assert res.status_code == 200
    cid = res.json()["comment_id"]

    res = client.get("/docs/doc1/comments")
    assert len(res.json()) == 1

    res = client.patch(f"/comments/{cid}", json={"status": "resolved"})
    assert res.json()["status"] == "resolved"

    rendered = client.get("/docs/doc1/render").json()
    assert "[comment:" in rendered["content"]


def test_toggle_comment_status(tmp_path: Path, monkeypatch):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    monkeypatch.setattr(api, "_store", rev_store)
    monkeypatch.setattr(api, "_comment_store", com_store)
    monkeypatch.setattr(api, "post_event", lambda e: None)
    client = TestClient(api.app)

    rev_store.save_document("doc", "content", "u1")
    comment = com_store.add_comment("doc", "L1", "u1", "n")

    res = client.post(f"/comments/{comment.comment_id}/toggle")
    assert res.status_code == 200
    assert res.json()["status"] == "resolved"
    res = client.post(f"/comments/{comment.comment_id}/toggle")
    assert res.json()["status"] == "open"


def test_document_view_endpoint(tmp_path: Path, monkeypatch):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    monkeypatch.setattr(api, "_store", rev_store)
    monkeypatch.setattr(api, "_comment_store", com_store)
    monkeypatch.setattr(api, "post_event", lambda e: None)
    client = TestClient(api.app)

    rev_store.save_document("doc", "line1", "u1")
    rev_store.save_document("doc", "line1\nline2", "u1")
    com_store.add_comment("doc", "L1", "u2", "note")

    res = client.get("/docs/doc/view")
    data = res.json()
    assert data["content"].startswith("line1")
    assert len(data["comments"]) == 1
    assert len(data["revisions"]) == 2
    assert data["revisions"][1]["diff"]


def test_concurrent_comment_writes(tmp_path: Path):
    store = CommentStore(tmp_path / "db.sqlite")

    def add(idx: int):
        store.add_comment("doc", "L1", "u", f"n{idx}")

    with ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(add, range(5))

    comments = store.list_comments("doc")
    assert len(comments) == 5
    assert [c["comment_id"] for c in comments] == [1, 2, 3, 4, 5]
