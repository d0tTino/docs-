from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agentauth.store import TokenStore, migrate_tokens_file  # noqa: E402


def test_token_store(tmp_path: Path):
    store = TokenStore(tmp_path / "tokens.json")
    token = store.create_token("agent1")
    assert store.verify(token.token) == "agent1"
    store.delete_token(token.token)
    assert store.verify(token.token) is None


def test_token_expiration(tmp_path: Path, monkeypatch):
    store = TokenStore(tmp_path / "tokens.json", ttl=1)
    token = store.create_token("agent1")
    orig_now = store._now
    monkeypatch.setattr(store, "_now", lambda: orig_now() + 2)
    assert store.verify(token.token) is None


def test_migrate_tokens(tmp_path: Path):
    path = tmp_path / "tokens.json"
    path.write_text(json.dumps({"tok": "agent1"}))
    migrate_tokens_file(path, ttl=60)
    store = TokenStore(path, ttl=60)
    assert "tok" not in path.read_text()
    assert store.verify("tok") == "agent1"
