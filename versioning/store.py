from __future__ import annotations

import difflib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


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
    """Persist and retrieve document revisions."""

    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            self.data: Dict[str, List[Dict]] = json.loads(path.read_text())
        else:
            self.data = {}

    def _write(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2))

    def list_revisions(self, document_id: str) -> List[Dict]:
        """Return all revisions for ``document_id``."""
        return self.data.get(document_id, [])

    def get_revision(self, document_id: str, version: int) -> Optional[Dict]:
        """Retrieve a specific revision."""
        for rev in self.data.get(document_id, []):
            if rev["version"] == version:
                return rev
        return None

    def _latest_content(self, document_id: str) -> str:
        revs = self.data.get(document_id, [])
        return revs[-1]["content"] if revs else ""

    def save_document(self, document_id: str, content: str, author_id: str) -> Revision:
        """Record a new revision for ``document_id``."""
        previous = self._latest_content(document_id)
        diff = "".join(
            difflib.unified_diff(
                previous.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile="previous",
                tofile="current",
            )
        )
        revisions = self.data.setdefault(document_id, [])
        revision = Revision(
            document_id=document_id,
            version=len(revisions) + 1,
            author_id=author_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            diff=diff,
            content=content,
        )
        revisions.append(asdict(revision))
        self._write()
        return revision

    def revert(self, document_id: str, version: int, author_id: str) -> Revision:
        """Revert ``document_id`` to ``version`` recording the action."""
        target = self.get_revision(document_id, version)
        if target is None:
            raise ValueError("Revision not found")
        return self.save_document(document_id, target["content"], author_id)
