import sqlite3
import json
from datetime import datetime, timedelta
import os
from theatrics import Me, pprint

def evidence(conn, cursor, session_id):
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

        # Create table if it doesn't exist
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

        # Cleanup old data
        cleanup(cursor)

        conn.commit()
        return conn, cursor

    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return None, None


def log(cursor, session_id, module, data, input_string=""):
    """Insert a log entry with optional quip."""

    timestamp = datetime.now().isoformat()
    me = Me()
    quip = me.quip(input_string)

    try:
        cursor.execute(
            "INSERT INTO evidence (session_id, timestamp, module, data, quip) VALUES (?, ?, ?, ?, ?)",
            (session_id, timestamp, module, json.dumps(data), quip)
        )
        cursor.connection.commit()
        return quip

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        cursor.connection.rollback()
        return None

def delete(cursor, evidence_id):
    cursor.execute("DELETE FROM evidence WHERE id=?", (evidence_id,))
    cursor.connection.commit()

def update(cursor, evidence_id, new_quip):
    cursor.execute(
        "UPDATE evidence SET quip=? WHERE id=?",
        (new_quip, evidence_id)
    )
    cursor.connection.commit()
