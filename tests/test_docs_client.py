from pathlib import Path
import sys
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from versioning import api  # noqa: E402
from versioning.client import ConflictError, DocsClient  # noqa: E402
from versioning.store import RevisionStore  # noqa: E402
from comments.store import CommentStore  # noqa: E402
from agentauth.store import TokenStore  # noqa: E402


def setup_client(
    tmp_path: Path,
) -> tuple[DocsClient, RevisionStore, CommentStore, TokenStore]:
    rev_store = RevisionStore(tmp_path / "rev.sqlite")
    com_store = CommentStore(tmp_path / "com.sqlite")
    token_store = TokenStore(tmp_path / "tok.json")
    api._store = rev_store
    api._comment_store = com_store
    api._token_store = token_store
    test_client = TestClient(api.app)
    token = token_store.create_token("agent1").token
    docs_client = DocsClient(test_client.base_url, token=token, session=test_client)
    api.post_event = lambda event: None
    return docs_client, rev_store, com_store, token_store


def test_update_document_end_to_end(tmp_path: Path):
    client, rev_store, _, _ = setup_client(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    client.update_document(
        "doc1",
        " world",
        author_id="agent1",
        summary="append",
        correlation_id="corr-1",
    )
    assert rev_store.list_revisions("doc1")[-1]["content"] == "hello world"


def test_update_document_conflict(tmp_path: Path):
    client, rev_store, _, _ = setup_client(tmp_path)
    rev_store.save_document("doc1", "a\nb\n", "agent1")
    rev_store.save_document("doc1", "a\nB\n", "agent2")
    try:
        client.update_document(
            "doc1",
            "a\nb2\n",
            author_id="agent1",
            summary="edit",
            append=False,
            base_version=1,
        )
    except ConflictError as exc:
        assert exc.latest == 2
        assert exc.conflicts
    else:
        assert False, "ConflictError not raised"


def test_create_comment(tmp_path: Path):
    client, rev_store, com_store, _ = setup_client(tmp_path)
    rev_store.save_document("doc1", "hello", "agent1")
    res = client.create_comment(
        "doc1",
        section_ref="L1",
        author_id="user1",
        body="note",
        correlation_id="corr-2",
    )
    assert res["body"] == "note"
    assert com_store.list_comments("doc1")[0]["body"] == "note"
