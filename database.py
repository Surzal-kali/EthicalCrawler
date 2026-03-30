import sqlite3
import json
from datetime import datetime, timedelta
import os
import time

DATABASE_PATH = "/tmp/li_evidence.db"

def init_db():
    """Create the evidence database and table."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Legacy table for high-level events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                module TEXT,
                data TEXT,
                quip TEXT
            )
        ''')

        # Narrator-aware debug log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                field TEXT,
                raw_value TEXT,
                normalized_key TEXT,
                persona TEXT,
                quip_text TEXT,
                context TEXT,
                timestamp REAL
            )
        ''')

        cleanup(cursor)
        conn.commit()
        return conn, cursor

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return None, None

def cleanup(cursor):
    """Deletes evidence older than 7 days."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    cursor.execute("DELETE FROM evidence WHERE timestamp < ?", (seven_days_ago.isoformat(),))
    cursor.connection.commit()

def log(cursor, session_id, field, raw_value, narrator, context="system_profiler"):
    """Store a fully annotated log entry for debugging and introspection."""
    normalized = narrator.normalize(field, raw_value)
    quip_text = narrator.quip(field, raw_value)

    cursor.execute(
        """
        INSERT INTO logs (session_id, field, raw_value, normalized_key, persona, quip_text, context, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            field,
            str(raw_value),  # Ensure it's a string
            normalized,
            narrator.persona,
            quip_text,
            context,
            time.time()
        )
    )
    cursor.connection.commit()