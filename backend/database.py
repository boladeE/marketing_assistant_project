import sqlite3
import os
from typing import List, Dict, Any
import datetime

class Database:
    def __init__(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        self.db_path = os.path.join(data_dir, "campaigns.db")
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()

    def get_all_campaigns(self) -> List[Dict[str, Any]]:
        """Retrieve all campaigns from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT prompt, content, timestamp FROM campaigns ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            return [
                {
                    "prompt": row[0],
                    "content": row[1],
                    "timestamp": row[2]
                }
                for row in rows
            ]

    def add_campaign(self, prompt: str, content: str) -> None:
        """Add a new campaign to the database."""
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO campaigns (prompt, content, timestamp) VALUES (?, ?, ?)',
                (prompt, content, timestamp)
            )
            conn.commit()

    def update_campaign(self, index: int, content: str) -> bool:
        """Update an existing campaign's content."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM campaigns ORDER BY timestamp DESC LIMIT 1 OFFSET ?', (index,))
            result = cursor.fetchone()
            if result:
                campaign_id = result[0]
                timestamp = datetime.datetime.now().isoformat()
                cursor.execute(
                    'UPDATE campaigns SET content = ?, timestamp = ? WHERE id = ?',
                    (content, timestamp, campaign_id)
                )
                conn.commit()
                return True
            return False

    def delete_campaign(self, index: int) -> bool:
        """Delete a campaign by its index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM campaigns ORDER BY timestamp DESC LIMIT 1 OFFSET ?', (index,))
            result = cursor.fetchone()
            if result:
                campaign_id = result[0]
                cursor.execute('DELETE FROM campaigns WHERE id = ?', (campaign_id,))
                conn.commit()
                return True
            return False 