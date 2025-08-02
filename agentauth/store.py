from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from secrets import token_hex
from typing import Dict, Optional


@dataclass
class Token:
    token: str
    agent_id: str


class TokenStore:
    """Persist and verify API tokens for agents."""

    def __init__(self, path: Path):
        self.path = path
        if path.exists():
            self.data: Dict[str, str] = json.loads(path.read_text())
        else:
            self.data = {}

    def _write(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2))

    def create_token(self, agent_id: str) -> Token:
        token = token_hex(16)
        self.data[token] = agent_id
        self._write()
        return Token(token=token, agent_id=agent_id)

    def delete_token(self, token: str) -> None:
        if token in self.data:
            del self.data[token]
            self._write()

    def verify(self, token: str) -> Optional[str]:
        return self.data.get(token)
