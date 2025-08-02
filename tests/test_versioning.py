from pathlib import Path

from versioning.store import RevisionStore
from versioning.render import render_document
from comments.store import CommentStore


def test_revision_save_and_list(tmp_path: Path):
    store = RevisionStore(tmp_path / "db.json")
    store.save_document("doc1", "Hello", "user1")
    store.save_document("doc1", "Hello world", "user1")

    revisions = store.list_revisions("doc1")
    assert [r["version"] for r in revisions] == [1, 2]

    rev2 = store.get_revision("doc1", 2)
    assert rev2["content"] == "Hello world"
    assert rev2["author_id"] == "user1"


def test_revert(tmp_path: Path):
    store = RevisionStore(tmp_path / "db.json")
    store.save_document("doc1", "First", "user1")
    store.save_document("doc1", "Second", "user1")

    store.revert("doc1", 1, "admin")
    latest = store.get_revision("doc1", 3)
    assert latest["content"] == "First"
    assert latest["author_id"] == "admin"


def test_diff_revisions(tmp_path: Path):
    store = RevisionStore(tmp_path / "db.json")
    store.save_document("doc1", "a", "u1")
    store.save_document("doc1", "ab", "u1")
    diff = store.diff_revisions("doc1", 1, 2)
    assert "-a" in diff and "+ab" in diff


def test_render_unresolved(tmp_path: Path):
    rev_store = RevisionStore(tmp_path / "rev.json")
    com_store = CommentStore(tmp_path / "com.json")
    rev_store.save_document("doc", "line1", "u1")
    com_store.add_comment("doc", "line1", "u2", "note")
    rendered = render_document("doc", rev_store, com_store)
    assert "comment:1!" in rendered["content"]
    assert rendered["comments"][0]["unresolved"]
