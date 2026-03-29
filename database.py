import sqlite3
import json
from datetime import datetime

def init_db(session_id):
    """Create the evidence database and table"""
    
    db_path = f"/tmp/local_inspector_{session_id}/evidence.db"
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
    
    conn.commit()
    return conn, cursor

def log(cursor, session_id, module, data):
    """Dump anything into the evidence bucket"""
    
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO evidence (session_id, timestamp, module, data)
        VALUES (?, ?, ?, ?)
    ''', (session_id, timestamp, module, json.dumps(data)))