import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file: str):
        # open a connection & use Row factory for convenient dict-like access
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.initialize_db()

    def initialize_db(self):
        c = self.conn.cursor()
        # table to hold a single watering flag (id is constrained to 1)
        c.execute("""
            CREATE TABLE IF NOT EXISTS watering (
                id     INTEGER PRIMARY KEY CHECK (id = 1),
                status INTEGER NOT NULL
            )
        """)
        # table to hold each log entry separately
        c.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT    NOT NULL,
                code INTEGER NOT NULL
            )
        """)
        # if the watering table is empty, insert the default row
        c.execute("SELECT COUNT(*) FROM watering")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO watering (id, status) VALUES (1, 0)")
        self.conn.commit()

    def update_watering(self, new_watering: bool):
        """Set watering flag to True or False."""
        c = self.conn.cursor()
        c.execute(
            "UPDATE watering SET status = ? WHERE id = 1",
            (1 if new_watering else 0,)
        )
        self.conn.commit()

    def log_watering(self, code: int):
        """Append a new log entry with current timestamp and the given code."""
        c = self.conn.cursor()
        now_iso = datetime.now().isoformat()
        c.execute(
            "INSERT INTO logs (date, code) VALUES (?, ?)",
            (now_iso, code)
        )
        self.conn.commit()

    def get_logs(self):
        """
        Return a list of all log entries, most‐recent first.
        Each entry is a dict: {'date': '…', 'code': …}.
        """
        c = self.conn.cursor()
        c.execute("SELECT date, code FROM logs ORDER BY id DESC")
        return [dict(row) for row in c.fetchall()]

    def get_watering(self) -> bool:
        """Return the current watering flag (True/False)."""
        c = self.conn.cursor()
        c.execute("SELECT status FROM watering WHERE id = 1")
        row = c.fetchone()
        return bool(row["status"]) if row else False

    def close(self):
        """Close the underlying SQLite connection."""
        self.conn.close()

    def __del__(self):
        # ensure connection is closed if the object is garbage-collected
        try:
            self.conn.close()
        except Exception:
            pass
