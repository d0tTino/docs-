from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

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


class CommentStore:
    """Persist and retrieve document comments using SQLite."""

    def __init__(self, path: Path):
        self.path = path
        with get_db(self.path) as db:
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

    def add_comment(
        self, document_id: str, section_ref: str, author_id: str, body: str
    ) -> Comment:
        now = datetime.now(timezone.utc).isoformat()
        with get_db(self.path) as db:
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
                (document_id, section_ref, author_id, body, "open", now),
            )
            comment_id = cur.lastrowid
        return Comment(
            comment_id=comment_id,
            document_id=document_id,
            section_ref=section_ref,
            author_id=author_id,
            body=body,
            status="open",
            created_at=now,
        )

    def list_comments(self, document_id: str) -> List[Dict]:
        with get_db(self.path) as db:
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
        return [dict(row) for row in rows]

    def get_comment(self, comment_id: int) -> Optional[Dict]:
        with get_db(self.path) as db:
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
        return dict(row) if row else None

    def update_comment(
        self, comment_id: int, body: Optional[str] = None, status: Optional[str] = None
    ) -> Optional[Dict]:
        with get_db(self.path) as db:
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
            data = dict(row)
            if body is not None:
                data["body"] = body
            if status is not None:
                data["status"] = status
            db.execute(
                "UPDATE comments SET body=?, status=? WHERE comment_id=?",
                (data["body"], data["status"], comment_id),
            )
        return data
