"""Utilities for ingesting markdown files into a local vector database."""

from __future__ import annotations

import argparse
import pickle
import re
from pathlib import Path
from typing import Iterable, List

import markdown


TOKEN_REGEX = re.compile(r"\b\w+\b", re.UNICODE)


def ingest_markdown(path: Path, chunk_size: int = 500) -> Iterable[str]:
    """Yield token chunks from markdown files."""
    text = Path(path).read_text(encoding="utf-8")
    tokens = TOKEN_REGEX.findall(markdown.markdown(text))
    for i in range(0, len(tokens), chunk_size):
        yield " ".join(tokens[i : i + chunk_size])


def embed(text: str) -> List[float]:
    """Return a simple numeric embedding for ``text``."""
    return [float(hash(text) % 1000000)]


class VectorDB:
    """Very small local vector database stub."""

    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            with path.open("rb") as f:
                self.data = pickle.load(f)
        else:
            self.data = []

    def add_texts(self, texts: Iterable[str]):
        embeddings = [embed(t) for t in texts]
        self.data.extend(zip(embeddings, texts))
        with self.path.open("wb") as f:
            pickle.dump(self.data, f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest markdown into a vector database"
    )
    parser.add_argument("input", type=Path, help="Markdown file to ingest")
    parser.add_argument(
        "--db",
        dest="db",
        type=Path,
        default=Path("vector_db.pkl"),
        help="Database file",
    )
    args = parser.parse_args()

    chunks = list(ingest_markdown(args.input))
    db = VectorDB(args.db)
    db.add_texts(chunks)


if __name__ == "__main__":
    main()
