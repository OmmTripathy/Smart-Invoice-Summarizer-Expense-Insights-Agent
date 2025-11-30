import sqlite3
import json
from pathlib import Path
from typing import Dict, Any
import os

# Define DB path relative to the current working directory
DB_DIR = Path("storage")
DB_PATH = DB_DIR / "sessions.db"
DB_DIR.mkdir(exist_ok=True) 

class SessionManager:
    """Manages session data using SQLite for persistence."""
    def __init__(self):
        self._create_table()

    def _create_table(self):
        """Creates the SQLite table if it does not exist."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                data TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save(self, session_id: str, data: Dict[str, Any]):
        """Saves or updates session data."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO sessions (session_id, data)
            VALUES (?, ?)
        """, (session_id, json.dumps(data)))
        conn.commit()
        conn.close()

    def load(self, session_id: str) -> Dict[str, Any] | None:
        """Loads session data by ID."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data FROM sessions WHERE session_id = ?", (session_id,))
        row = c.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None