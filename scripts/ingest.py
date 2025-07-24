"""Simple markdown ingest script."""
from pathlib import Path

import markdown


def ingest_markdown(path: Path, chunk_size: int = 500):
    """Yield text chunks from markdown files."""
    text = Path(path).read_text()
    html = markdown.markdown(text)
    words = html.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])


if __name__ == "__main__":
    for chunk in ingest_markdown(Path("../ai-research/logical-chunking.md")):
        print(len(chunk.split()))
