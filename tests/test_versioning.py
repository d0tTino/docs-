from pathlib import Path

from versioning.store import RevisionStore


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
