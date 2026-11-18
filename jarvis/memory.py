"""SQLite-backed conversation history and notes. Everything stays on your own machine."""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path


class Memory:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS messages ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT NOT NULL, "
            "role TEXT NOT NULL, content TEXT NOT NULL, "
            "created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, "
            "created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        self._conn.commit()

    # -- conversation -------------------------------------------------
    def add(self, session: str, role: str, content: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO messages (session, role, content) VALUES (?, ?, ?)",
                (session, role, content),
            )
            self._conn.commit()

    def history(self, session: str, limit: int = 20) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT role, content FROM messages WHERE session = ? ORDER BY id DESC LIMIT ?",
                (session, limit),
            ).fetchall()
        return [{"role": r, "content": c} for r, c in reversed(rows)]

    def clear(self, session: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM messages WHERE session = ?", (session,))
            self._conn.commit()

    # -- notes --------------------------------------------------------
    def add_note(self, text: str) -> int:
        with self._lock:
            cur = self._conn.execute("INSERT INTO notes (text) VALUES (?)", (text,))
            self._conn.commit()
            return int(cur.lastrowid)

    def list_notes(self) -> list[tuple[int, str, str]]:
        with self._lock:
            return self._conn.execute("SELECT id, text, created FROM notes ORDER BY id").fetchall()

    def delete_note(self, note_id: int) -> bool:
        with self._lock:
            cur = self._conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            self._conn.commit()
            return cur.rowcount > 0

    def close(self) -> None:
        with self._lock:
            self._conn.close()
