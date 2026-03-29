import sqlite3
import json
from datetime import datetime
from theatrics import Me

def init_db(session_id):
    """Create the evidence database and table"""

    db_path = f"/tmp/local_inspector_{session_id}/evidence.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # One simple table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                module TEXT,
                data TEXT
            )
        ''')

        # Add quip column if it doesn't exist
        cursor.execute('''
            ALTER TABLE IF NOT EXISTS evidence
            ADD COLUMN quip TEXT
        ''')

        conn.commit()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return None  # Return None if initialization fails


def log(cursor, session_id, module, data, input_string=""):
    """Dump anything into the evidence bucket with optional quip."""
    
    timestamp = datetime.now().isoformat()
    me = Me()
    quip = me.quip(input_string) # Use the input to get a quip

    sql = "INSERT INTO evidence (session_id, timestamp, module, data, quip) VALUES (?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (session_id, timestamp, module, json.dumps(data), quip))
        cursor.connection.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        cursor.connection.rollback()
        return None

    return quip