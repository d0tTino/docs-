from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


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
    """Persist and retrieve document comments."""

    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            self.data: Dict[str, List[Dict]] = json.loads(path.read_text())
        else:
            self.data = {"comments": []}

    def _write(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2))

    def _next_id(self) -> int:
        return len(self.data["comments"]) + 1

    def add_comment(
        self, document_id: str, section_ref: str, author_id: str, body: str
    ) -> Comment:
        comment = Comment(
            comment_id=self._next_id(),
            document_id=document_id,
            section_ref=section_ref,
            author_id=author_id,
            body=body,
            status="open",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.data["comments"].append(asdict(comment))
        self._write()
        return comment

    def list_comments(self, document_id: str) -> List[Dict]:
        return [c for c in self.data["comments"] if c["document_id"] == document_id]

    def get_comment(self, comment_id: int) -> Optional[Dict]:
        for c in self.data["comments"]:
            if c["comment_id"] == comment_id:
                return c
        return None

    def update_comment(
        self, comment_id: int, body: Optional[str] = None, status: Optional[str] = None
    ) -> Optional[Dict]:
        comment = self.get_comment(comment_id)
        if comment is None:
            return None
        if body is not None:
            comment["body"] = body
        if status is not None:
            comment["status"] = status
        self._write()
        return comment
