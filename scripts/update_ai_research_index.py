#!/usr/bin/env python3
"""Update docs/ai-research/index.md with a sorted list of documents."""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs" / "ai-research"
INDEX_FILE = DOCS_DIR / "index.md"


def _extract_title(path: Path) -> str:
    """Return the title from the markdown file at ``path``."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^title:\s*\"?([^\n\"]+)\"?", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return path.stem.replace("-", " ").title()


def build_index() -> str:
    """Construct the index markdown content."""
    items = []
    for md in sorted(DOCS_DIR.glob("*.md")):
        if md.name == "index.md":
            continue
        title = _extract_title(md)
        items.append((title, md.name))
    items.sort(key=lambda x: x[0].lower())

    lines = [
        "---",
        'title: "AI Research"',
        "tags: [research, docs]",
        'project: "ai-research"',
        f"updated: {_dt.date.today()}",
        "---",
        "",
        "# AI Research",
        "",
        "## Documents",
    ]
    for title, filename in items:
        lines.append(f"- [{title}]({filename})")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    content = build_index()
    INDEX_FILE.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
