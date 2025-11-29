import sqlite3
import json
import os

DB_PATH = os.path.join(os.getcwd(), "storage", "sessions.db")

class SessionManager:
    def __init__(self):
        self._create_table()

    def _create_table(self):
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

    def save(self, session_id: str, data: dict):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO sessions (session_id, data)
            VALUES (?, ?)
        """, (session_id, json.dumps(data)))
        conn.commit()
        conn.close()

    def load(self, session_id: str):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data FROM sessions WHERE session_id = ?", (session_id,))
        row = c.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None
