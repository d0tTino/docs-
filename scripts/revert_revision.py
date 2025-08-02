from __future__ import annotations

import argparse
from pathlib import Path

from versioning.store import RevisionStore


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Revert a document to a specific revision",
    )
    parser.add_argument("document_id", help="Document identifier")
    parser.add_argument("version", type=int, help="Revision number to revert to")
    parser.add_argument(
        "--author",
        default="admin",
        help="Author performing the revert",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("revision_store.json"),
        help="Revision database file",
    )
    args = parser.parse_args()

    store = RevisionStore(args.db)
    store.revert(args.document_id, args.version, args.author)
    print(f"Reverted {args.document_id} to revision {args.version}")


if __name__ == "__main__":
    main()
