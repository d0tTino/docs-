from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from scripts.ingest import ingest_markdown, VectorDB  # noqa: E402


def test_ingest_chunking(tmp_path):
    content = "This is a simple test file with enough words to form multiple chunks."
    md_file = tmp_path / "sample.md"
    md_file.write_text(content)

    chunks = list(ingest_markdown(md_file, chunk_size=3))

    assert chunks == [
        "This is a",
        "simple test file",
        "with enough words",
        "to form multiple",
        "chunks.",
    ]


def test_cli_chunk_size_and_persistence(tmp_path):
    content = "Alpha beta gamma delta epsilon zeta"
    md_file = tmp_path / "upload.md"
    md_file.write_text(content)

    db_file = tmp_path / "db.pkl"

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/ingest.py"),
            str(md_file),
            "--db",
            str(db_file),
            "--chunk-size",
            "2",
        ],
        check=True,
    )

    db = VectorDB(db_file)
    assert len(db.data) == 3

    reloaded = VectorDB(db_file)
    assert reloaded.data == db.data


def test_embed_deterministic():
    script = (
        "import sys; "
        f"sys.path.append('{str(ROOT)}'); "
        "from scripts.ingest import embed; "
        "print(embed('deterministic'))"
    )
    result1 = subprocess.check_output([sys.executable, "-c", script])
    result2 = subprocess.check_output([sys.executable, "-c", script])
    assert result1 == result2


def test_vector_db_query(tmp_path):
    text = "Alpha beta gamma delta epsilon"
    md_file = tmp_path / "query.md"
    md_file.write_text(text)

    db_file = tmp_path / "db.pkl"
    chunks = list(ingest_markdown(md_file, chunk_size=2))
    db = VectorDB(db_file)
    db.add_texts(chunks)

    assert db.query("gamma delta") == ["gamma delta"]
    results = db.query("some query", top_k=2)
    assert len(results) == 2


def test_ingest_empty_file(tmp_path):
    md_file = tmp_path / "empty.md"
    md_file.write_text("")
    assert list(ingest_markdown(md_file)) == []


def test_vector_db_query_empty(tmp_path):
    db_file = tmp_path / "empty.pkl"
    db = VectorDB(db_file)
    assert db.query("anything") == []
