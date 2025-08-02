from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass
from typing import Optional

import requests

UME_EVENT_ENDPOINT = "https://ume.example.com/events"
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds


@dataclass
class EventPayload:
    document_id: str
    event_type: str
    author_id: str
    timestamp: str
    revision_id: Optional[int]
    correlation_id: Optional[str] = None


def post_event(event: EventPayload) -> None:
    """POST an event to the UME ingestion endpoint with retries."""
    payload = asdict(event)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            res = requests.post(UME_EVENT_ENDPOINT, json=payload, timeout=5)
            res.raise_for_status()
            return
        except Exception as exc:  # pragma: no cover - logging of all failures
            logging.warning(
                "Failed to send UME event (attempt %s/%s): %s",
                attempt,
                MAX_RETRIES,
                exc,
            )
            time.sleep(RETRY_DELAY)
    logging.error(
        "Giving up sending UME event after %s attempts", MAX_RETRIES
    )
