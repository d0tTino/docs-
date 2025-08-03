from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from db import get_db


@dataclass
class Subscription:
    """Subscriber preferences for a document."""

    document_id: str
    subscriber_id: str
    channels: List[str]


class SubscriptionStore:
    """Persist and retrieve notification subscriptions using SQLite."""

    def __init__(self, path: Path):
        self.path = path
        with get_db(self.path) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS subscriptions (
                    document_id TEXT,
                    subscriber_id TEXT,
                    channels TEXT,
                    PRIMARY KEY (document_id, subscriber_id)
                )
                """
            )

    def subscribe(
        self, document_id: str, subscriber_id: str, channels: List[str]
    ) -> None:
        """Add or update a subscription."""
        with get_db(self.path) as db:
            db.execute(
                """
                INSERT INTO subscriptions (document_id, subscriber_id, channels)
                VALUES (?, ?, ?)
                ON CONFLICT(document_id, subscriber_id)
                    DO UPDATE SET channels=excluded.channels
                """,
                (document_id, subscriber_id, json.dumps(channels)),
            )

    def unsubscribe(self, document_id: str, subscriber_id: str) -> None:
        """Remove a subscription if present."""
        with get_db(self.path) as db:
            db.execute(
                "DELETE FROM subscriptions WHERE document_id=? AND subscriber_id=?",
                (document_id, subscriber_id),
            )

    def get_subscribers(self, document_id: str) -> List[Dict]:
        """Return all subscriptions for ``document_id``."""
        with get_db(self.path) as db:
            rows = db.execute(
                """
                SELECT document_id, subscriber_id, channels
                FROM subscriptions WHERE document_id=?
                """,
                (document_id,),
            ).fetchall()
        result: List[Dict] = []
        for row in rows:
            data = dict(row)
            data["channels"] = json.loads(data["channels"])
            result.append(data)
        return result
