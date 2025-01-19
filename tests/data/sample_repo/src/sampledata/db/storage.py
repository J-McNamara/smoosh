"""Database operations module."""
import sqlite3
from typing import List, Dict, Any
from pathlib import Path

class DBStorage:
    """Handle database operations."""

    def __init__(self, db_path: Path):
        """Initialize database connection."""
        self.db_path = db_path

    def store_results(self, results: List[Dict[str, Any]]) -> None:
        """Store analysis results in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results
                (id INTEGER PRIMARY KEY, timestamp TEXT, data TEXT)
            """)

            for result in results:
                cursor.execute(
                    "INSERT INTO results (timestamp, data) VALUES (?, ?)",
                    (result['timestamp'], str(result['data']))
                )
