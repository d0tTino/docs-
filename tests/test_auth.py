from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agentauth.store import TokenStore  # noqa: E402


def test_token_store(tmp_path: Path):
    store = TokenStore(tmp_path / "tokens.json")
    token = store.create_token("agent1")
    assert store.verify(token.token) == "agent1"
    store.delete_token(token.token)
    assert store.verify(token.token) is None
