from pathlib import Path
import sys
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from versioning import api  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from comments.store import CommentStore  # noqa: E402
from agentauth.store import TokenStore  # noqa: E402


def setup_app(tmp_path: Path):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    token_store = TokenStore(tmp_path / "tok.json")
    api._store = rev_store
    api._comment_store = com_store
    api._token_store = token_store
    client = TestClient(api.app)
    return client, rev_store, com_store, token_store


def test_put_doc_append(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    com_store.add_comment("doc1", "L1", "user1", "note")
    token = token_store.create_token("agent1").token
    calls = []
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: calls.append((d, s)))
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.put(
        "/docs/doc1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": " world",
            "author_id": "agent1",
            "summary": "append test",
            "append": True,
        },
    )
    assert res.status_code == 200
    assert rev_store.list_revisions("doc1")[-1]["content"] == "hello world"
    assert calls == [("doc1", "append test")]


def test_put_doc_replace(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    token = token_store.create_token("agent1").token
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: None)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.put(
        "/docs/doc1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "new",
            "author_id": "agent1",
            "summary": "replace test",
            "append": False,
        },
    )
    assert res.status_code == 200
    assert rev_store.list_revisions("doc1")[-1]["content"] == "new"


def test_put_doc_auth(tmp_path: Path):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    token_store.create_token("agent1")
    res = client.put(
        "/docs/doc1",
        headers={"Authorization": "Bearer wrong"},
        json={
            "content": " world",
            "author_id": "agent1",
            "summary": "append test",
            "append": True,
        },
    )
    assert res.status_code == 401


def test_put_doc_conflict(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "a\nb\n", "agent1")
    rev_store.save_document("doc1", "a\nB\n", "agent2")
    token = token_store.create_token("agent1").token
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: None)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.put(
        "/docs/doc1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "a\nb2\n",
            "author_id": "agent1",
            "summary": "edit",
            "append": False,
            "base_version": 1,
        },
    )
    assert res.status_code == 409
    detail = res.json()["detail"]
    assert "diff" in detail and "conflicts" in detail and detail["conflicts"]


def test_diff_endpoint(tmp_path: Path):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "a", "agent1")
    rev_store.save_document("doc1", "ab", "agent1")
    res = client.get("/docs/doc1/diff/1/2")
    assert res.status_code == 200
    assert "-a" in res.json()["diff"]


def test_resolve_doc(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "a\nb\n", "agent1")
    rev_store.save_document("doc1", "a\nB\n", "agent2")
    token = token_store.create_token("agent1").token
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: None)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/resolve",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "a\nB2\n",
            "author_id": "agent1",
            "summary": "merge",
            "base_version": 2,
        },
    )
    assert res.status_code == 200
    assert rev_store.list_revisions("doc1")[-1]["content"] == "a\nB2\n"


def test_resolve_doc_conflict(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "a\nb\n", "agent1")
    rev_store.save_document("doc1", "a\nB\n", "agent2")
    token = token_store.create_token("agent1").token
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: None)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/resolve",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "a\nb2\n",
            "author_id": "agent1",
            "summary": "merge",
            "base_version": 1,
        },
    )
    assert res.status_code == 409
    assert res.json()["detail"]["conflicts"]
