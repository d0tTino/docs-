from pathlib import Path
from fastapi.testclient import TestClient
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from versioning import api  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from comments.store import CommentStore  # noqa: E402
from agentauth.store import TokenStore  # noqa: E402
from notifications.store import SubscriptionStore  # noqa: E402


def setup_app(tmp_path: Path):
    rev_store = RevisionStore(tmp_path / "rev.json")
    com_store = CommentStore(tmp_path / "com.json")
    token_store = TokenStore(tmp_path / "tok.json")
    sub_store = SubscriptionStore(tmp_path / "sub.json")
    api._store = rev_store
    api._comment_store = com_store
    api._token_store = token_store
    api._subscription_store = sub_store
    client = TestClient(api.app)
    return client, rev_store, com_store, token_store, sub_store


def test_revision_notification(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    token = token_store.create_token("agent1").token
    sub_store.subscribe("doc1", "user1", ["email"])

    sent = []
    monkeypatch.setattr(
        api, "_send_notification", lambda s, c, p: sent.append((s, c, p))
    )
    monkeypatch.setattr(api, "post_event", lambda e: None)
    monkeypatch.setattr(api, "_notify_comments", lambda d, s: None)

    res = client.put(
        "/docs/doc1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "hello",
            "author_id": "agent1",
            "summary": "s",
            "append": False,
        },
    )
    assert res.status_code == 200
    assert sent[0][0] == "user1"
    assert sent[0][2]["revision_id"] == 1


def test_comment_notification_unsub(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    client.post(
        "/docs/doc1/subscriptions",
        json={"subscriber_id": "user1", "channels": ["email"]},
    )
    client.delete("/docs/doc1/subscriptions/user1")

    sent = []
    monkeypatch.setattr(
        api, "_send_notification", lambda s, c, p: sent.append((s, c, p))
    )
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/comments",
        json={"section_ref": "L1", "author_id": "u1", "body": "note"},
    )
    assert res.status_code == 200
    assert sent == []


def test_comment_notification_payload(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    rev = rev_store.save_document("doc1", "hello", "agent1")
    client.post(
        "/docs/doc1/subscriptions",
        json={"subscriber_id": "user1", "channels": ["websocket"]},
    )

    sent = []
    monkeypatch.setattr(
        api, "_send_notification", lambda s, c, p: sent.append((s, c, p))
    )
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/comments",
        json={"section_ref": "L1", "author_id": "u1", "body": "note"},
    )
    assert res.status_code == 200
    assert sent[0][2]["revision_id"] == rev.version
    assert sent[0][2]["comment_link"].endswith("/comments/1")
