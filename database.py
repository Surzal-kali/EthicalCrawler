import sqlite3
import json
from datetime import datetime, timedelta
import os
import time
import tempfile
from pathlib import Path

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

        # Session persistence table - tracks user state across runs
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

        # Quips table - user-editable commentary per data type/persona combination
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                persona TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at REAL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(key, persona, text)
            )
        ''')

        # Seed default quips if table is empty
        _seed_default_quips(cursor)

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

def save_session(cursor, session_id: str, username: str, persona: str, closeness: float, slip_intensity: float):
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
    
    # If no rows updated, insert new
    if cursor.rowcount == 0:
        cursor.execute(
            """
            INSERT INTO sessions (id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (session_id, username, persona, closeness, slip_intensity, current_time, current_time)
        )
    
    cursor.connection.commit()

def _seed_default_quips(cursor):
    """Seed database with default quips from theatrics.py templates. Runs only if table is empty."""
    cursor.execute("SELECT COUNT(*) FROM quips")
    if cursor.fetchone()[0] > 0:
        return  # Already seeded
    
    from theatrics import TEMPLATES, MIMIC_VOICE
    
    # Seed TEMPLATES quips (shared across personas)
    for key, quips in TEMPLATES.items():
        if isinstance(quips, str):
            quips = [quips]
        for quip_text in quips:
            try:
                cursor.execute(
                    "INSERT INTO quips (key, persona, text) VALUES (?, ?, ?)",
                    (key, "all", quip_text)
                )
            except sqlite3.IntegrityError:
                pass  # Duplicate, skip
    
    # Seed MIMIC_VOICE quips (persona-specific)
    for persona, key_quips in MIMIC_VOICE.items():
        for key, quip_text in key_quips.items():
            if isinstance(quip_text, str):
                quip_text = [quip_text]
            else:
                quip_text = quip_text if isinstance(quip_text, list) else [str(quip_text)]
            
            for text in quip_text:
                try:
                    cursor.execute(
                        "INSERT INTO quips (key, persona, text) VALUES (?, ?, ?)",
                        (key, persona, text)
                    )
                except sqlite3.IntegrityError:
                    pass  # Duplicate, skip
    
    cursor.connection.commit()

def get_quip(cursor, key: str, persona: str) -> str:
    """
    Get a quip from the database. Checks persona-specific first, then falls back to "all".
    Returns the quip text, or a generic fallback if not found.
    """
    # Try persona-specific first
    cursor.execute(
        "SELECT text FROM quips WHERE key = ? AND persona = ? ORDER BY RANDOM() LIMIT 1",
        (key, persona)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Fall back to "all" (generic)
    cursor.execute(
        "SELECT text FROM quips WHERE key = ? AND persona = 'all' ORDER BY RANDOM() LIMIT 1",
        (key,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    
    # Final fallback
    return f"{key}. Another piece. I'll keep it."

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