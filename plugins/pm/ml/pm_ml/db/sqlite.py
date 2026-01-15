"""SQLite database access for PM ML service."""

import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class DatabaseManager:
    """Shared database access to pm.db"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to .claude/pm.db
            home = Path.home()
            db_path = str(home / ".claude" / "pm.db")

        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Get or create database connection"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results as list of dicts"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """Execute SELECT query and return first result as dict"""
        results = self.query(sql, params)
        return results[0] if results else None

    def execute(self, sql: str, params: Optional[tuple] = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.rowcount

    def close(self):
        """Close database connection"""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
