#!/usr/bin/env python3
"""Update docs/non-ai-research/index.md with a sorted list of documents."""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs" / "non-ai-research"
INDEX_FILE = DOCS_DIR / "index.md"


def _extract_title(path: Path) -> str:
    """Return the title from the markdown file at ``path``."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^title:[ \t]*\"?([^\n\"]+)\"?", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    match = re.search(
        r"^title:\s*\n\s+\"([^\n\"]*(?:\n\s+[^\n\"]*)*)\"",
        text,
        re.MULTILINE,
    )
    if match:
        return " ".join(line.strip() for line in match.group(1).splitlines())
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
        'title: "Non-AI Research"',
        "tags: [research, docs]",
        'project: "non-ai-research"',
        f"updated: {_dt.date.today()}",
        "---",
        "",
        "# Non-AI Research",
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
