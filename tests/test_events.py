import pytest
import requests

from ume import events


def test_post_event_retries_with_exponential_backoff(monkeypatch):
    event = events.EventPayload(
        document_id="doc1",
        event_type="test",
        author_id="author",
        timestamp="2024-01-01T00:00:00Z",
        revision_id=None,
    )

    calls = []

    def fake_post(url, json, timeout):
        calls.append(1)
        raise requests.RequestException("boom")

    monkeypatch.setattr(events.requests, "post", fake_post)

    delays = []

    def fake_sleep(seconds):
        delays.append(seconds)

    monkeypatch.setattr(events.time, "sleep", fake_sleep)

    with pytest.raises(requests.RequestException):
        events.post_event(event)

    assert len(calls) == events.MAX_RETRIES
    expected_delays = [
        min(2 ** attempt, events.MAX_BACKOFF)
        for attempt in range(1, events.MAX_RETRIES)
    ]
    assert delays == expected_delays
