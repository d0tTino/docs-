from __future__ import annotations

import json
import hashlib
import time
from dataclasses import dataclass
from pathlib import Path
from secrets import token_hex
from typing import Dict, Optional


@dataclass
class Token:
    token: str
    agent_id: str
    expires: int


class TokenStore:
    """Persist and verify API tokens for agents."""

    def __init__(self, path: Path, ttl: int = 3600):
        self.path = path
        self.ttl = ttl
        if path.exists():
            self.data: Dict[str, Dict[str, int]] = json.loads(path.read_text())
        else:
            self.data = {}
        self.cleanup()

    def _write(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2))

    def _now(self) -> int:
        return int(time.time())

    def _digest(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def create_token(self, agent_id: str) -> Token:
        token = token_hex(16)
        digest = self._digest(token)
        expires = self._now() + self.ttl
        self.data[digest] = {"agent_id": agent_id, "expires": expires}
        self._write()
        return Token(token=token, agent_id=agent_id, expires=expires)

    def delete_token(self, token: str) -> None:
        digest = self._digest(token)
        if digest in self.data:
            del self.data[digest]
            self._write()

    def verify(self, token: str) -> Optional[str]:
        self.cleanup()
        digest = self._digest(token)
        info = self.data.get(digest)
        if info and info["expires"] > self._now():
            return info["agent_id"]
        return None

    def cleanup(self) -> None:
        now = self._now()
        expired = [d for d, info in self.data.items() if info["expires"] <= now]
        if expired:
            for d in expired:
                del self.data[d]
            self._write()


def migrate_tokens_file(path: Path, ttl: int = 3600) -> None:
    """Migrate a plaintext token file to hashed format with expiration."""
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return
    if data and all(isinstance(v, dict) and "agent_id" in v for v in data.values()):
        return
    now = int(time.time())
    new_data = {}
    for token, agent_id in data.items():
        digest = hashlib.sha256(token.encode()).hexdigest()
        new_data[digest] = {"agent_id": agent_id, "expires": now + ttl}
    path.write_text(json.dumps(new_data, indent=2))
