import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import time
import tempfile
from pathlib import Path

from quips import get_catalog_quip, iter_catalog_quips

def get_evidence_dir() -> Path:
    """
    Get platform-aware directory for evidence database.
    Uses system temp directory by default.
    On Windows: C:\\Users\\<user>\\AppData\\Local\\Temp\\ethical_crawler
    On Unix: /tmp/ethical_crawler or similar
    """
    temp_dir = Path(tempfile.gettempdir()) / "ethical_crawler"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir

DATABASE_PATH = get_evidence_dir() / "li_evidence.db"


def seed_default_quips(cursor):
    """Backfill default quips without overwriting user-added rows."""
    for key, persona, text in iter_catalog_quips():
        cursor.execute(
            "INSERT OR IGNORE INTO quips (key, persona, text) VALUES (?, ?, ?)",
            (key, persona, text)
        )


def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,       
            persona TEXT NOT NULL,      
            text TEXT NOT NULL,
            mood TEXT DEFAULT 'neutral', 
            weight INTEGER DEFAULT 1,   
            created_at REAL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(key, persona, text)
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_quips_lookup ON quips(key, persona)')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_config (
            mood TEXT PRIMARY KEY,
            intensity INTEGER DEFAULT 0,
            min_closeness INTEGER DEFAULT 0,
            max_closeness INTEGER DEFAULT 100
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personalities (
            seed_hash TEXT PRIMARY KEY,
            base_persona TEXT DEFAULT 'foothold',
            base_slip_intensity REAL DEFAULT 5,
            affinity_tags TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            name TEXT
            quip TEXT
            closeness_impact REAL
            session_impact REAL
        
                   
        )
    '''
)


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            persona TEXT DEFAULT 'foothold',
            closeness REAL DEFAULT 0,
            slip_intensity REAL DEFAULT 5,
            created_at REAL NOT NULL,
            last_accessed REAL NOT NULL,
            session_count INTEGER DEFAULT 1
        )
    ''')
    
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

    seed_default_quips(cursor)
    conn.commit()
    return conn, cursor

def save_evidence(cursor, session_id, module, data, quip):
    """Save a piece of evidence to the database."""
    cursor.execute(
        "INSERT INTO evidence (session_id, timestamp, module, data, quip) VALUES (?, ?, ?, ?, ?)",
        (session_id, datetime.now().isoformat(), module, json.dumps(data), quip)
    )
    cursor.connection.commit()
#i see what you mean
def cleanup(cursor):
    """Remove entries older than 30 days to prevent database bloat."""
    cutoff_time = time.time() - (30 * 24 * 60 * 60)  # 30 days in seconds
    cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_time,))
    cursor.execute("DELETE FROM sessions WHERE last_accessed < ?", (cutoff_time,))
    cursor.connection.commit()
 
def log(cursor, session_id, field, raw_value, narrator, context="system_profiler"):
    """Store a fully annotated log entry for debugging and introspection."""
    normalized = narrator.normalize(field, raw_value)
    quip_text = narrator.quip(field, raw_value, cursor=cursor)



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

def load_session(cursor, username: str):
    """Load existing session state by username. Returns dict or None if not found."""
    cursor.execute(
        """
        SELECT id, persona, closeness, slip_intensity, created_at, last_accessed, session_count
        FROM sessions WHERE username = ?
        """,
        (username,)
    )
    row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'username': username,
            'persona': row[1],
            'closeness': row[2],
            'slip_intensity': row[3],
            'created_at': row[4],
            'last_accessed': row[5],
            'session_count': row[6]
        }
    return None
#that should do the trick right?
# let me sit on that 
def save_session(cursor, session_id, username, persona, closeness, slip_intensity):
    """Save or update session state. Called at session end."""
    current_time = time.time()
    
    # Try to update existing
    cursor.execute(
        """
        UPDATE sessions 
        SET persona = ?, closeness = ?, slip_intensity = ?, last_accessed = ?, session_count = session_count + 1
        WHERE username = ?
        """,
        (persona, closeness, slip_intensity, current_time, username)
    )
    #but it already does that?
    #
    # If no rows updated, insert new
    if cursor.rowcount == 0:
        cursor.execute(
            """
            INSERT INTO sessions (id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, username, persona, closeness, slip_intensity, current_time, current_time, 1)
        )
    else:
        #just like that? 
        #just like that 
        pass  # Existing session updated
    cursor.connection.commit()

def get_quip(cursor, key: str, persona: str) -> str:
    """
    Get a quip from the database. Checks persona-specific first, then falls back to "all".
    Returns the quip text, or a generic fallback if not found.
    """
    line = get_catalog_quip(key, persona)
    if line:
        return line

    cursor.execute(
        "SELECT text FROM quips WHERE key = ? AND persona = ? ORDER BY RANDOM() LIMIT 1",
        (key, persona)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor.execute(
        "SELECT text FROM quips WHERE key = ? AND persona = 'all' ORDER BY RANDOM() LIMIT 1",
        (key,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Final fallback
    return get_catalog_quip(key, persona) or f"{key}. Another piece. I'll keep it."

def add_quip(cursor, key: str, persona: str, text: str) -> bool:
    """Add a new quip to the database. Returns True if added, False if duplicate."""
    try:
        cursor.execute(
            "INSERT INTO quips (key, persona, text) VALUES (?, ?, ?)",
            (key, persona, text)
        )
        cursor.connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Duplicate entry