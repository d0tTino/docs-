#!/usr/bin/env python3
"""Inline snippet markers in Markdown files.

This script searches for lines matching the pattern ``--8<-- "path"`` in the
provided Markdown files and replaces them with the contents of the referenced
file. Paths are resolved relative to the documentation root directory, which
defaults to ``docs`` under the repository root but can be overridden with
``--docs-dir``.

Usage:
    python scripts/expand_snippets.py [--docs-dir DIR] file [file ...]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

SNIPPET_RE = re.compile(r"^--8<--\s+\"([^\"]+)\"\s*\n?", re.MULTILINE)


def expand_file(md_file: Path, docs_dir: Path) -> None:
    """Replace snippet markers in ``md_file``."""
    text = md_file.read_text(encoding="utf-8")

    def repl(match: re.Match[str]) -> str:
        rel_path = match.group(1)
        snippet_path = docs_dir / rel_path
        if not snippet_path.is_file():
            raise FileNotFoundError(f"snippet not found: {rel_path}")
        return snippet_path.read_text(encoding="utf-8")

    new_text = SNIPPET_RE.sub(repl, text)
    md_file.write_text(new_text, encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files to expand")
    parser.add_argument(
        "--docs-dir",
        default=Path(__file__).resolve().parent.parent / "docs",
        type=Path,
        help="Base directory for snippet paths",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    for md_file in args.files:
        expand_file(md_file, args.docs_dir)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
