"""Persistencia local de eventos para la fase mock de la POC.

La interfaz del repositorio es deliberadamente pequeña para poder sustituir
SQLite por DynamoDB cuando llegue la integración AWS.
"""

import json
import sqlite3
from pathlib import Path


class EventStore:
    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def is_empty(self) -> bool:
        with self._connect() as connection:
            row = connection.execute('SELECT COUNT(*) AS total FROM events').fetchone()
            return row['total'] == 0

    def list(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute('SELECT payload FROM events ORDER BY rowid DESC').fetchall()
        return [json.loads(row['payload']) for row in rows]

    def save(self, event: dict) -> dict:
        with self._connect() as connection:
            connection.execute(
                'INSERT OR REPLACE INTO events (event_id, payload) VALUES (?, ?)',
                (event['id'], json.dumps(event, ensure_ascii=False)),
            )
        return event
