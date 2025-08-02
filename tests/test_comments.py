from pathlib import Path
import sys
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from comments.store import CommentStore  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from versioning import api  # noqa: E402


def test_comment_store(tmp_path: Path):
    store = CommentStore(tmp_path / "db.json")
    c1 = store.add_comment("doc1", "L1-2", "user1", "note")
    assert c1.comment_id == 1
    assert store.list_comments("doc1")[0]["body"] == "note"

    store.update_comment(1, status="resolved")
    assert store.get_comment(1)["status"] == "resolved"


def test_comment_endpoints(tmp_path: Path, monkeypatch):
    rev_store = RevisionStore(tmp_path / "rev.json")
    com_store = CommentStore(tmp_path / "com.json")
    monkeypatch.setattr(api, "_store", rev_store)
    monkeypatch.setattr(api, "_comment_store", com_store)
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
