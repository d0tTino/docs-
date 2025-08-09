#!/usr/bin/env python3
"""Scan Markdown files for mid-word line splits.

This script checks Markdown files in a given directory for lines that end
with a letter when the following line begins with a letter. Such patterns often
indicate a word that was accidentally split across lines. An optional ``--fix``
flag rewrites files in place to automatically join the split words.

Usage:
    python scripts/lint_research_docs.py [--fix] [PATH ...]

The command exits with status 1 if any potential issues are found (unless
``--fix`` is specified).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List


def find_splits(path: Path, fix: bool = False) -> List[str]:
    """Return a list of lint error messages for ``path``.

    If ``fix`` is True, detected splits are joined and the file is rewritten.
    """

    errors: List[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    ends_with_newline = text.endswith("\n")

    idx = 0
    while idx < len(lines) - 1:
        line = lines[idx]
        next_line = lines[idx + 1]
        if line and line[-1].isalpha() and next_line and next_line[0].isalpha():
            errors.append(f"{path}:{idx + 1}: possible mid-word split")
            if fix:
                lines[idx] = line + next_line
                del lines[idx + 1]
                continue  # re-check same index in case of multiple splits
        idx += 1

    if fix and errors:
        new_text = "\n".join(lines)
        if ends_with_newline:
            new_text += "\n"
        path.write_text(new_text, encoding="utf-8")

    return errors


def scan_paths(paths: Iterable[Path], fix: bool = False) -> List[str]:
    """Scan the provided paths for issues."""
    errors: List[str] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            errors.extend(find_splits(path, fix=fix))
        elif path.is_dir():
            for md_file in path.rglob("*.md"):
                errors.extend(find_splits(md_file, fix=fix))
    return errors


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite files in place to join detected mid-word splits",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("docs/ai-research")],
        help="Files or directories to scan",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    errors = scan_paths(args.paths, fix=args.fix)
    if errors and not args.fix:
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
