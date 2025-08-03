from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
import sys
import smtplib
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from versioning import api  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from comments.store import CommentStore  # noqa: E402
from agentauth.store import TokenStore  # noqa: E402
from notifications.store import SubscriptionStore  # noqa: E402


def setup_app(tmp_path: Path):
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    token_store = TokenStore(tmp_path / "tok.json")
    sub_store = SubscriptionStore(tmp_path / "sub.sqlite")
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

    class DummySMTP:
        def __init__(self, *a, **kw):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def send_message(self, msg):  # pragma: no cover - simple capture
            sent.append(msg)

    monkeypatch.setattr(smtplib, "SMTP", lambda *a, **kw: DummySMTP())
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
    assert len(sent) == 1


def test_comment_notification_unsub(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    client.post(
        "/docs/doc1/subscriptions",
        json={"subscriber_id": "user1", "channels": ["webhook"]},
    )
    client.delete("/docs/doc1/subscriptions/user1")

    calls = []
    monkeypatch.setattr(
        requests, "post", lambda url, json, timeout=3: calls.append((url, json))
    )
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/comments",
        json={"section_ref": "L1", "author_id": "u1", "body": "note"},
    )
    assert res.status_code == 200
    assert calls == []


def test_comment_notification_payload(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    rev = rev_store.save_document("doc1", "hello", "agent1")
    client.post(
        "/docs/doc1/subscriptions",
        json={"subscriber_id": "user1", "channels": ["webhook"]},
    )

    calls = []

    def fake_post(url, json, timeout=3):  # pragma: no cover - network stub
        calls.append((url, json))

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(api, "post_event", lambda e: None)

    res = client.post(
        "/docs/doc1/comments",
        json={"section_ref": "L1", "author_id": "u1", "body": "note"},
    )
    assert res.status_code == 200
    assert calls[0][1]["revision_id"] == rev.version
    assert calls[0][1]["comment_link"].endswith("/comments/1")


def test_comment_author_notified_on_revision(tmp_path: Path, monkeypatch):
    client, rev_store, com_store, token_store, sub_store = setup_app(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    com_store.add_comment("doc1", "L1", "user1", "note")
    token = token_store.create_token("agent1").token

    sent = []

    class DummySMTP:
        def __init__(self, *a, **kw):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def send_message(self, msg):  # pragma: no cover - simple capture
            sent.append(msg)

    monkeypatch.setattr(smtplib, "SMTP", lambda *a, **kw: DummySMTP())
    monkeypatch.setattr(api, "post_event", lambda e: None)
    monkeypatch.setattr(api, "_notify_subscribers", lambda *a, **kw: None)

    res = client.put(
        "/docs/doc1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": " world",
            "author_id": "agent1",
            "summary": "update",
            "append": True,
        },
    )
    assert res.status_code == 200
    assert len(sent) == 1


def test_concurrent_subscribe(tmp_path: Path):
    store = SubscriptionStore(tmp_path / "sub.sqlite")

    def sub(i: int):
        store.subscribe("doc", f"u{i}", ["email"])

    with ThreadPoolExecutor(max_workers=5) as ex:
        ex.map(sub, range(5))

    subs = store.get_subscribers("doc")
    assert len(subs) == 5
