#!/usr/bin/env python3
"""Update docs/ai-research/index.md with a sorted list of documents."""

from __future__ import annotations

import datetime as _dt
import re
from collections import defaultdict
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
    """Construct the index markdown content grouped by directory."""
    groups: dict[Path, list[tuple[str, Path]]] = defaultdict(list)
    for md in sorted(DOCS_DIR.rglob("*.md")):
        if md.name == "index.md":
            continue
        rel_path = md.relative_to(DOCS_DIR)
        title = _extract_title(md)
        groups[rel_path.parent].append((title, rel_path))

    lines = [
        "---",
        'title: "AI Research"',
        "tags: [research, docs]",
        'project: "ai-research"',
        f"updated: {_dt.date.today()}",
        "---",
        "",
        '--8<-- "_snippets/disclaimer.md"',
        "",
        "# AI Research",
        "",
        "## Documents",
    ]

    # Root-level documents (no subdirectory)
    root_items = groups.pop(Path("."), []) + groups.pop(Path(""), [])
    for title, rel in sorted(root_items, key=lambda x: x[0].lower()):
        lines.append(f"- [{title}]({rel.as_posix()})")

    # Subdirectories
    for directory in sorted(groups):
        heading = directory.name.replace("-", " ").title()
        lines.append("")
        lines.append(f"### {heading}")
        for title, rel in sorted(groups[directory], key=lambda x: x[0].lower()):
            lines.append(f"- [{title}]({rel.as_posix()})")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    content = build_index()
    INDEX_FILE.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
