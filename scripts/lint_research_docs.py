#!/usr/bin/env python3
"""Scan Markdown files for formatting, metadata, and accessibility.

This script checks Markdown files in a given directory for common formatting
issues. It flags lines that end with a letter when the following line begins
with a letter (a sign of a word accidentally split across lines) and lines that
contain extraneous trailing spaces. It also verifies that each file contains
required front matter metadata and the standard disclaimer snippet, and
reports image tags with empty alt text.

Usage:
    python scripts/lint_research_docs.py [--path PATH]

The command exits with status 1 if any potential issues are found.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Iterable, List


def find_splits(path: Path) -> List[str]:
    """Return a list of lint error messages for ``path``."""
    errors: List[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    # Front matter and disclaimer checks
    disclaimer = '--8<-- "_snippets/disclaimer.md"'
    content_start = 0
    if lines and lines[0].strip() == "---":
        try:
            end_idx = lines[1:].index("---") + 1
        except ValueError:
            errors.append(f"{path}: missing closing front matter delimiter")
            end_idx = 0
        else:
            front_matter = lines[1:end_idx]
            required = ["title", "tags", "project", "updated"]
            for key in required:
                if not any(line.startswith(f"{key}:") for line in front_matter):
                    errors.append(f"{path}: missing '{key}' in front matter")
        snippet_section = lines[end_idx + 1:]
        if disclaimer in snippet_section:
            snippet_idx = end_idx + 1 + snippet_section.index(disclaimer)
            content_start = snippet_idx + 1
        else:
            errors.append(f"{path}: missing disclaimer snippet")
            content_start = end_idx + 1
    else:
        errors.append(f"{path}: missing front matter")
        snippet_section = lines
        if disclaimer in snippet_section:
            snippet_idx = snippet_section.index(disclaimer)
            content_start = snippet_idx + 1
        else:
            errors.append(f"{path}: missing disclaimer snippet")

    # Existing whitespace and split checks for content only
    md_img_pattern = re.compile(r'!\[\s*\]\([^)]*\)')
    html_img_pattern = re.compile(r"<img[^>]*alt=([\'\"])\s*\1", re.IGNORECASE)

    for idx, line in enumerate(lines[content_start:], start=content_start):
        if line.rstrip() != line:
            errors.append(f"{path}:{idx + 1}: trailing whitespace")
        if idx < len(lines) - 1 and line and line[-1].isalpha():
            next_line = lines[idx + 1]
            if next_line and next_line[0].isalpha():
                errors.append(f"{path}:{idx + 1}: possible mid-word split")
        if md_img_pattern.search(line) or html_img_pattern.search(line):
            errors.append(f"{path}:{idx + 1}: image with empty alt text")
    return errors


def scan_paths(paths: Iterable[Path]) -> List[str]:
    """Scan the provided paths for issues."""
    errors: List[str] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            errors.extend(find_splits(path))
        elif path.is_dir():
            for md_file in path.rglob("*.md"):
                errors.extend(find_splits(md_file))
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("docs/ai-research")],
        help="Files or directories to scan",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    errors = scan_paths(args.paths)
    if errors:
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
