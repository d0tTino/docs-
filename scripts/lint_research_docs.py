#!/usr/bin/env python3
"""Scan Markdown files for mid-word line splits.

This script checks Markdown files in a given directory for lines that end
with a letter when the following line begins with a letter. Such patterns often
indicate a word that was accidentally split across lines.

Usage:
    python scripts/lint_research_docs.py [--path PATH]

The command exits with status 1 if any potential issues are found.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List


def find_splits(path: Path) -> List[str]:
    """Return a list of lint error messages for ``path``."""
    errors: List[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for idx, line in enumerate(lines[:-1]):
        if line and line[-1].isalpha():
            next_line = lines[idx + 1]
            if next_line and next_line[0].isalpha():
                errors.append(f"{path}:{idx + 1}: possible mid-word split")
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
