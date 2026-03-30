import sqlite3
import json
from datetime import datetime, timedelta
import os
from theatrics import Me, pprint
import time
def display_evidence(cursor, session_id):
    """Print formatted evidence for a session."""
    cursor.execute("SELECT * FROM evidence WHERE session_id=?", (session_id,))
    results = cursor.fetchall()
    
    for row in results:
        evidence_id = row[0]
        module = row[3]
        data = json.loads(row[4])
        quip = row[5]
        
        pprint(
            f"[{evidence_id}] Module: {module}\n"
            f"    Value: {data.get('value')}\n"
            f"    Quip: {quip}"
        )
    
    return results

def get_evidence(cursor, session_id):
    """Return raw evidence data."""
    cursor.execute("SELECT * FROM evidence WHERE session_id=?", (session_id,))
    return cursor.fetchall()

def cleanup(cursor):
    """Deletes evidence older than 7 days."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    cursor.execute("DELETE FROM evidence WHERE timestamp < ?", (seven_days_ago.isoformat(),))
    cursor.connection.commit()

def init_db(session_id):
    """Create the evidence database and table."""

    base_dir = f"/tmp/local_inspector_{session_id}"
    os.makedirs(base_dir, exist_ok=True)

    db_path = f"{base_dir}/evidence.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Legacy table (still useful for high-level events)
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

        # New narrator-aware debug log table
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


def log(cursor, session_id, field, raw_value, narrator, context="system_profiler"):
    """
    Store a fully annotated log entry for debugging and introspection.
    """

    normalized = narrator.normalize(field, raw_value)
    quip_text = narrator.quip(field, raw_value)

    entry = {
        "session_id": session_id,
        "field": field,
        "raw_value": raw_value,
        "normalized_key": normalized,
        "persona": narrator.persona,
        "quip_text": quip_text,
        "context": context,
        "timestamp": time.time()
    }

    cursor.execute(
        """
        INSERT INTO logs (session_id, field, raw_value, normalized_key, persona, quip_text, context, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry["session_id"],
            entry["field"],
            entry["raw_value"],
            entry["normalized_key"],
            entry["persona"],
            entry["quip_text"],
            entry["context"],
            entry["timestamp"]
        )
    )

    return entry

def delete(cursor, evidence_id):
    cursor.execute("DELETE FROM evidence WHERE id=?", (evidence_id,))
    cursor.connection.commit()

def update(cursor, evidence_id, new_quip):
    cursor.execute(
        "UPDATE evidence SET quip=? WHERE id=?",
        (new_quip, evidence_id)
    )
    cursor.connection.commit()
