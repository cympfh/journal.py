import datetime
import json
import os
import sqlite3
from typing import Any

from fastapi import Body, FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="journal.py", version="1.0.0")
db = None


class Database:
    def __init__(self):
        self.path = os.getenv("DATABASE_PATH", "journal.db")
        self.connection = sqlite3.connect(self.path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

        # Debug output: show database path and sample data
        print(f"Database initialized at: {self.path}")
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM journal")
        count = cursor.fetchone()["count"]
        print(f"Total records in database: {count}")

        if count > 0:
            cursor.execute(
                "SELECT section, key, timestamp FROM journal ORDER BY timestamp LIMIT 3"
            )
            sample_rows = cursor.fetchall()
            print("Sample records:")
            for row in sample_rows:
                print(f"  {row['timestamp']} - {row['section']}/{row['key']}")
        else:
            print("Database is empty")

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS journal (
                section TEXT,
                key TEXT,
                data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (section, key, timestamp)
            )
            """
        )
        self.connection.commit()

    def get_entries(
        self, section: str, key: str, tail: int = 10, from_timestamp: str | None = None
    ):
        cursor = self.connection.cursor()

        if from_timestamp:
            # Normalize timestamp format - if it's just YYYY-MM-DD, add T00:00:00.000Z
            if len(from_timestamp) == 10 and from_timestamp.count("-") == 2:
                from_timestamp = from_timestamp + "T00:00:00.000Z"
            elif len(from_timestamp) == 19 and "T" in from_timestamp:
                from_timestamp = from_timestamp + ".000Z"

            cursor.execute(
                """
                SELECT section, key, data, timestamp
                FROM journal 
                WHERE section = ? AND key = ? AND timestamp >= ?
                ORDER BY timestamp
                LIMIT ?
                """,
                (section, key, from_timestamp, tail),
            )
        else:
            cursor.execute(
                """
                SELECT section, key, data, timestamp
                FROM journal
                WHERE section = ? AND key = ?
                ORDER BY timestamp
                LIMIT ?
                """,
                (section, key, tail),
            )
        return cursor.fetchall()

    def insert_entry(
        self, section: str, key: str, data: str, timestamp: str | None = None
    ):
        cursor = self.connection.cursor()
        if timestamp:
            cursor.execute(
                "INSERT INTO journal (section, key, data, timestamp) VALUES (?, ?, ?, ?)",
                (section, key, data, timestamp),
            )
        else:
            cursor.execute(
                "INSERT INTO journal (section, key, data) VALUES (?, ?, ?)",
                (section, key, data),
            )
        self.connection.commit()


class JournalEntry(BaseModel):
    section: str
    key: str
    data: Any
    timestamp: str


@app.get("/journal/{section}/{key}")
def get_journal(
    section: str,
    key: str,
    tail: int = Query(default=10, description="Number of entries to return"),
    from_timestamp: str | None = Query(
        default=None, alias="from", description="Start timestamp (YYYY-MM-DD HH:MM:SS)"
    ),
    reverse: bool = Query(
        default=False, description="Reverse order (DESC instead of ASC)"
    ),
) -> list[JournalEntry]:
    if db is None:
        return []

    rows = db.get_entries(section, key, tail, from_timestamp)
    entries = [
        JournalEntry(
            section=row["section"],
            key=row["key"],
            data=json.loads(row["data"]),
            timestamp=row["timestamp"],
        )
        for row in rows
    ]
    if reverse:
        entries.reverse()
    return entries


@app.post("/journal/{section}/{key}")
def post_journal(
    section: str,
    key: str,
    data: Any = Body(...),
    timestamp: str | None = Query(default=None),
):
    if db is None:
        return {"error": "Database not initialized"}

    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp_str = timestamp or now.isoformat()
    data_json = json.dumps(data)

    db.insert_entry(section, key, data_json, timestamp_str)

    entry = JournalEntry(
        section=section,
        key=key,
        data=data_json,
        timestamp=timestamp_str,
    )
    return entry


db = Database()
