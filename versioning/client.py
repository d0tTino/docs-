"""Client wrapper for the docs versioning API.

Example:
    from versioning.client import DocsClient
    client = DocsClient("http://localhost:8000", token="secrettoken")
    client.update_document("doc1", "content", author_id="agent1", summary="demo")
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


class ConflictError(Exception):
    """Raised when the server reports a version conflict."""

    def __init__(self, diff: str, latest: int, conflicts: Any):
        super().__init__("document update conflict")
        self.diff = diff
        self.latest = latest
        self.conflicts = conflicts


@dataclass
class DocsClient:
    """Simple client for interacting with the versioning API.

    Parameters
    ----------
    base_url:
        Base URL of the running API server.
    token:
        Bearer token used for authentication.
    session:
        Optional ``requests`` compatible session. This is primarily useful
        for injecting ``TestClient`` during unit tests.
    """

    base_url: str
    token: str
    session: Optional[requests.sessions.Session] = None

    def __post_init__(self) -> None:
        self.base_url = str(self.base_url).rstrip("/")
        self._session = self.session or requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {self.token}"})

    # Internal request helper
    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers: Dict[str, str] = {}
        if correlation_id:
            # send in header for cross-service tracing
            headers["X-Correlation-ID"] = correlation_id
            if json is not None:
                json.setdefault("correlation_id", correlation_id)
            else:
                json = {"correlation_id": correlation_id}
        resp = self._session.request(method, url, json=json, headers=headers)
        return resp

    def update_document(
        self,
        doc_id: str,
        content: str,
        author_id: str,
        summary: str,
        *,
        append: bool = True,
        base_version: Optional[int] = None,
        correlation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "content": content,
            "author_id": author_id,
            "summary": summary,
            "append": append,
        }
        if base_version is not None:
            payload["base_version"] = base_version
        resp = self._request(
            "PUT",
            f"/docs/{doc_id}",
            json=payload,
            correlation_id=correlation_id,
        )
        if resp.status_code == 409:
            detail = resp.json().get("detail", {})
            raise ConflictError(
                detail.get("diff", ""),
                detail.get("latest", 0),
                detail.get("conflicts", []),
            )
        resp.raise_for_status()
        return resp.json()

    def create_comment(
        self,
        doc_id: str,
        section_ref: str,
        author_id: str,
        body: str,
        *,
        correlation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "section_ref": section_ref,
            "author_id": author_id,
            "body": body,
        }
        resp = self._request(
            "POST",
            f"/docs/{doc_id}/comments",
            json=payload,
            correlation_id=correlation_id,
        )
        resp.raise_for_status()
        return resp.json()
