"""List markdown files in docs/security."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECURITY_DIR = ROOT / "docs" / "security"


def list_files() -> None:
    """Print all markdown files in the security docs directory."""
    for path in sorted(SECURITY_DIR.glob("*.md")):
        print(path.name)


if __name__ == "__main__":
    list_files()
