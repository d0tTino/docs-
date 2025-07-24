from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.ingest import ingest_markdown


def test_ingest_chunking(tmp_path):
    content = "This is a simple test file with enough words to form multiple chunks."
    md_file = tmp_path / "sample.md"
    md_file.write_text(content)

    chunks = list(ingest_markdown(md_file, chunk_size=3))

    assert chunks == [
        "<p>This is a",
        "simple test file",
        "with enough words",
        "to form multiple",
        "chunks.</p>",
    ]


def test_db_upload_stub(tmp_path):
    content = "Alpha beta gamma delta epsilon zeta"
    md_file = tmp_path / "upload.md"
    md_file.write_text(content)

    uploaded = []

    def upload_stub(chunk):
        uploaded.append(chunk)

    for chunk in ingest_markdown(md_file, chunk_size=2):
        upload_stub(chunk)

    assert uploaded == [
        "<p>Alpha beta",
        "gamma delta",
        "epsilon zeta</p>",
    ]
