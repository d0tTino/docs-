from __future__ import annotations

import difflib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from db import get_db


@dataclass
class Revision:
    """Representation of a single document revision."""

    document_id: str
    version: int
    author_id: str
    timestamp: str
    diff: str
    content: str


class RevisionStore:
    """Persist and retrieve document revisions using SQLite."""

    def __init__(self, path: Path):
        self.path = path
        with get_db(self.path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS revisions (
                    document_id TEXT,
                    version INTEGER,
                    author_id TEXT,
                    timestamp TEXT,
                    diff TEXT,
                    content TEXT,
                    PRIMARY KEY (document_id, version)
                )
                """
            )

    def list_revisions(self, document_id: str) -> List[Dict]:
        """Return all revisions for ``document_id``."""
        with get_db(self.path) as db:
            rows = db.execute(
                "SELECT document_id, version, author_id, timestamp, diff, content\n"
                "FROM revisions WHERE document_id=? ORDER BY version",
                (document_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_revision(self, document_id: str, version: int) -> Optional[Dict]:
        """Retrieve a specific revision."""
        with get_db(self.path) as db:
            row = db.execute(
                "SELECT document_id, version, author_id, timestamp, diff, content\n"
                "FROM revisions WHERE document_id=? AND version=?",
                (document_id, version),
            ).fetchone()
        return dict(row) if row else None

    def _latest_content(self, document_id: str) -> str:
        with get_db(self.path) as db:
            row = db.execute(
                "SELECT content FROM revisions WHERE document_id=?\n"
                "ORDER BY version DESC LIMIT 1",
                (document_id,),
            ).fetchone()
        return row["content"] if row else ""

    def save_document(
        self,
        document_id: str,
        content: str,
        author_id: str,
        base_version: Optional[int] = None,
    ) -> Revision:
        """Record a new revision for ``document_id``.

        If ``base_version`` is provided the operation will fail with ``ValueError``
        when the stored latest version does not match, allowing callers to
        implement optimistic locking.
        """
        with get_db(self.path) as db:
            row = db.execute(
                "SELECT version, content FROM revisions WHERE document_id=?\n"
                "ORDER BY version DESC LIMIT 1",
                (document_id,),
            ).fetchone()
            previous = row["content"] if row else ""
            latest = row["version"] if row else 0
            if base_version is not None and base_version != latest:
                raise ValueError("Version mismatch")
            diff = "".join(
                difflib.unified_diff(
                    previous.splitlines(keepends=True),
                    content.splitlines(keepends=True),
                    fromfile="previous",
                    tofile="current",
                )
            )
            version = latest + 1
            revision = Revision(
                document_id=document_id,
                version=version,
                author_id=author_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                diff=diff,
                content=content,
            )
            db.execute(
                """
                INSERT INTO revisions (
                    document_id,
                    version,
                    author_id,
                    timestamp,
                    diff,
                    content
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    revision.document_id,
                    revision.version,
                    revision.author_id,
                    revision.timestamp,
                    revision.diff,
                    revision.content,
                ),
            )
        return revision

    def revert(self, document_id: str, version: int, author_id: str) -> Revision:
        """Revert ``document_id`` to ``version`` recording the action."""
        target = self.get_revision(document_id, version)
        if target is None:
            raise ValueError("Revision not found")
        return self.save_document(document_id, target["content"], author_id)

    def diff_revisions(
        self, document_id: str, from_version: int, to_version: int
    ) -> str:
        """Return unified diff between two revisions.

        Raises ``ValueError`` if either revision does not exist.
        """
        rev_from = self.get_revision(document_id, from_version)
        rev_to = self.get_revision(document_id, to_version)
        if rev_from is None or rev_to is None:
            raise ValueError("Revision not found")
        return "".join(
            difflib.unified_diff(
                rev_from["content"].splitlines(keepends=True),
                rev_to["content"].splitlines(keepends=True),
                fromfile=f"v{from_version}",
                tofile=f"v{to_version}",
            )
        )
