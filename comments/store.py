from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List, Optional

from db import get_db


@dataclass
class Comment:
    """Representation of a document comment."""

    comment_id: int
    document_id: str
    section_ref: str
    author_id: str
    body: str
    status: str
    created_at: str


class CommentStatus(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"


class CommentStore:
    """Persist and retrieve document comments using SQLite."""

    def __init__(self, path: Path):
        self.path = path
        with get_db(self.path, "write") as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS comments (
                    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id TEXT,
                    section_ref TEXT,
                    author_id TEXT,
                    body TEXT,
                    status TEXT,
                    created_at TEXT
                )
                """
            )
            # Ensure fast lookups when listing comments for a document.
            # `IF NOT EXISTS` allows this to run against existing databases
            # without failing if the index has already been created.
            db.execute(
                "CREATE INDEX IF NOT EXISTS idx_comments_doc ON comments(document_id)"
            )

    def add_comment(
        self, document_id: str, section_ref: str, author_id: str, body: str
    ) -> Comment:
        now = datetime.now(timezone.utc).isoformat()
        with get_db(self.path, "write") as db:
            cur = db.execute(
                """
                INSERT INTO comments (
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    CommentStatus.OPEN.value,
                    now,
                ),
            )
            comment_id = cur.lastrowid
        return Comment(
            comment_id=comment_id,
            document_id=document_id,
            section_ref=section_ref,
            author_id=author_id,
            body=body,
            status=CommentStatus.OPEN.value,
            created_at=now,
        )

    def _row_to_comment(self, row) -> Comment:
        data = dict(row)
        return Comment(**data)

    def list_comments(self, document_id: str) -> List[Comment]:
        with get_db(self.path, "read") as db:
            rows = db.execute(
                """
                SELECT
                    comment_id,
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    status,
                    created_at
                FROM comments WHERE document_id=? ORDER BY comment_id
                """,
                (document_id,),
            ).fetchall()
        return [self._row_to_comment(row) for row in rows]

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        with get_db(self.path, "read") as db:
            row = db.execute(
                """
                SELECT
                    comment_id,
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    status,
                    created_at
                FROM comments WHERE comment_id=?
                """,
                (comment_id,),
            ).fetchone()
        return self._row_to_comment(row) if row else None

    def update_comment(
        self, comment_id: int, body: Optional[str] = None, status: Optional[str] = None
    ) -> Optional[Comment]:
        with get_db(self.path, "write") as db:
            row = db.execute(
                """
                SELECT
                    comment_id,
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    status,
                    created_at
                FROM comments WHERE comment_id=?
                """,
                (comment_id,),
            ).fetchone()
            if row is None:
                return None
            comment = self._row_to_comment(row)
            if body is not None:
                comment.body = body
            if status is not None:
                try:
                    comment.status = CommentStatus(status).value
                except ValueError as exc:
                    raise ValueError("Invalid status") from exc

            db.execute(
                "UPDATE comments SET body=?, status=? WHERE comment_id=?",
                (comment.body, comment.status, comment_id),
            )
        return comment

    def toggle_comment(self, comment_id: int) -> Comment:
        """Flip a comment's status between ``open`` and ``resolved``."""
        with get_db(self.path, "write") as db:
            row = db.execute(
                """
                SELECT
                    comment_id,
                    document_id,
                    section_ref,
                    author_id,
                    body,
                    status,
                    created_at
                FROM comments WHERE comment_id=?
                """,
                (comment_id,),
            ).fetchone()
            if row is None:
                raise ValueError("Comment not found")
            comment = self._row_to_comment(row)
            if comment.status == CommentStatus.OPEN.value:
                new_status = CommentStatus.RESOLVED.value
            elif comment.status == CommentStatus.RESOLVED.value:
                new_status = CommentStatus.OPEN.value
            else:
                raise ValueError(f"Cannot toggle unknown status: {comment.status}")
            db.execute(
                "UPDATE comments SET status=? WHERE comment_id=?",
                (new_status, comment_id),
            )
        comment.status = new_status
        return comment
