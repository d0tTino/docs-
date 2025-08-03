from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class Subscription:
    """Subscriber preferences for a document."""

    document_id: str
    subscriber_id: str
    channels: List[str]


class SubscriptionStore:
    """Persist and retrieve notification subscriptions."""

    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            self.data: List[Dict] = json.loads(path.read_text()).get(
                "subscriptions", []
            )
        else:
            self.data = []

    def _write(self) -> None:
        self.path.write_text(json.dumps({"subscriptions": self.data}, indent=2))

    def subscribe(
        self, document_id: str, subscriber_id: str, channels: List[str]
    ) -> None:
        """Add or update a subscription."""
        for sub in self.data:
            if (
                sub["document_id"] == document_id
                and sub["subscriber_id"] == subscriber_id
            ):
                sub["channels"] = channels
                self._write()
                return
        self.data.append(asdict(Subscription(document_id, subscriber_id, channels)))
        self._write()

    def unsubscribe(self, document_id: str, subscriber_id: str) -> None:
        """Remove a subscription if present."""
        self.data = [
            s
            for s in self.data
            if not (
                s["document_id"] == document_id
                and s["subscriber_id"] == subscriber_id
            )
        ]
        self._write()

    def get_subscribers(self, document_id: str) -> List[Dict]:
        """Return all subscriptions for ``document_id``."""
        return [s for s in self.data if s["document_id"] == document_id]
