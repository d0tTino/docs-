from contextlib import contextmanager
import sqlite3
from pathlib import Path
from typing import Iterator


@contextmanager
def get_db(path: Path, mode: str = "read") -> Iterator[sqlite3.Connection]:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        if mode == "read":
            conn.execute("BEGIN")
        elif mode == "write":
            conn.execute("BEGIN IMMEDIATE")
        else:
            raise ValueError("mode must be 'read' or 'write'")
        yield conn
        conn.commit()
    finally:
        conn.close()
