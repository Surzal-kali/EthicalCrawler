import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import time
import tempfile
from pathlib import Path

from quips import get_catalog_quip, iter_catalog_quips
from tkinter import filedialog
from theatrics import Me, dev_comment, test, pprint, sudo, equip #oh yeah thanks. 
from consentform import ConsentKey

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
DEBUG_ENV_VAR = "ETHICAL_CRAWLER_DEBUG"


def _debug_enabled(debug=False):
    if debug:
        return True
    return os.getenv(DEBUG_ENV_VAR, "").strip().lower() in {"1", "true", "yes", "on"}


def _debug_print(enabled, message):
    if enabled:
        print(f"[DEBUG][database] {message}")


def _json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (set, tuple)):
        return list(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _safe_json_dumps(data):
    return json.dumps(data, default=_json_default)


def _canonical_username(username: str) -> str:
    """Normalize usernames so session lookup/save is case-insensitive."""
    return (username or "").strip().lower()


def seed_default_quips(cursor):
    """Backfill default quips without overwriting user-added rows."""
    for key, persona, text in iter_catalog_quips():
        cursor.execute(
            "INSERT OR IGNORE INTO quips (key, persona, text) VALUES (?, ?, ?)",
            (key, persona, text)
        )


# ---------------------------------------------------------------------------
# Mood behavior tree
# Each row: (mood, intensity, min_closeness, max_closeness, min_slip, max_slip, persona)
# persona='any' matches all personas; use a specific persona name to gate a mood.
# Multiple rows can match simultaneously — determine_mood picks one at random.
# ---------------------------------------------------------------------------
_MOOD_TREE = [
    ("neutral",    0,  0,  30, 0.0,  7.0,  "any"),
    ("distant",    1,  0,  30, 0.0, 10.0,  "any"),
    ("analytical", 3, 30,  60, 0.0,  8.0,  "any"),
    ("probing",    4, 30,  60, 3.0, 15.0,  "any"),
    ("curious",    6, 60,  99, 0.0, 10.0,  "any"),
    ("intrigued",  7, 60,  99, 5.0, 15.0,  "any"),
    ("fixated",    9, 60,  99, 8.0, 20.0,  "any"),
    ("hungry",    12,  0,  99, 8.0, 20.0,  "sudo"),
    ("unstable",  14,  0,  99,12.0, 20.0,  "sudo"),
    ("possessive",16, 60,  99,10.0, 20.0,  "sudo"),
    ("overloaded",18, 80,  99,15.0, 20.0,  "sudo"),
]


def seed_mood_config(cursor):
    """Populate mood_config with the default behavior tree rows if the table is empty."""
    cursor.execute("SELECT COUNT(*) FROM mood_config")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            """
            INSERT INTO mood_config
                (mood, intensity, min_closeness, max_closeness, min_slip, max_slip, persona)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            _MOOD_TREE,
        )


#should we give the cursor a class all its own?
#like a database manager or something? yeah
#it could handle all the queries and stuff and we just call methods on it
#fairenough, we can refactor later if it gets too unwieldy. for now it's pretty straightforward.

def init_db(debug=False):
    debug_mode = _debug_enabled(debug)
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''   
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at REAL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )   
        ''')
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

        _migrate_mood_config(cursor)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                intensity INTEGER DEFAULT 0,
                min_closeness REAL DEFAULT 0,
                max_closeness REAL DEFAULT 100,
                min_slip REAL DEFAULT 0,
                max_slip REAL DEFAULT 20,
                persona TEXT DEFAULT 'any'
            )
        ''')
        seed_mood_config(cursor)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                name TEXT NOT NULL,
                quip TEXT,
                closeness_impact REAL,
                session_impact REAL
            )
        ''')

        cursor.execute(
            '''
            DELETE FROM services
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM services
                GROUP BY session_id, name
            )
            '''
        )

        cursor.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS idx_services_session_name ON services(session_id, name)'
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

        _migrate_sessions_usernames(cursor)

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


        if debug_mode:
            seed_default_quips(cursor)
        conn.commit()
        return conn, cursor
    except (sqlite3.Error, OSError) as exc:
        if conn:
            try:
                conn.rollback()
            except sqlite3.Error:
                pass
            conn.close()
        _debug_print(debug_mode, f"init_db failed: {exc}")
        return None, None


def _migrate_mood_config(cursor):
    """Replace old mood_config schema with the behavior-tree-compatible schema."""
    cursor.execute("PRAGMA table_info(mood_config)")
    cols = {row[1] for row in cursor.fetchall()}
    # Old schemas lacked min_slip; drop and let init_db recreate with correct schema.
    if cols and 'min_slip' not in cols:
        cursor.execute("DROP TABLE IF EXISTS mood_config")


def _migrate_sessions_usernames(cursor):
    """Merge legacy mixed-case usernames into a canonical lowercase record."""
    cursor.execute(
        """
        SELECT id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count
        FROM sessions
        ORDER BY last_accessed DESC
        """
    )
    rows = cursor.fetchall()
    if not rows:
        return

    groups = {}
    for row in rows:
        key = _canonical_username(row[1])
        if not key:
            continue
        groups.setdefault(key, []).append(row)

    for canonical_username, grouped_rows in groups.items():
        if len(grouped_rows) == 1 and grouped_rows[0][1] == canonical_username:
            continue

        primary = grouped_rows[0]
        canonical_id = f"LI:{canonical_username}"
        merged_session_count = sum(r[7] or 0 for r in grouped_rows)

        for extra in grouped_rows[1:]:
            cursor.execute("DELETE FROM sessions WHERE id = ?", (extra[0],))

        cursor.execute(
            """
            UPDATE sessions
            SET id = ?,
                username = ?,
                persona = ?,
                closeness = ?,
                slip_intensity = ?,
                created_at = ?,
                last_accessed = ?,
                session_count = ?
            WHERE id = ?
            """,
            (
                canonical_id,
                canonical_username,
                primary[2],
                primary[3],
                primary[4],
                primary[5],
                primary[6],
                merged_session_count,
                primary[0],
            ),
        )

def save_evidence(cursor, session_id, module, data, quip):
    """Save a piece of evidence to the database."""
    cursor.execute(
        "INSERT INTO evidence (session_id, timestamp, module, data, quip) VALUES (?, ?, ?, ?, ?)",
        (session_id, datetime.now().isoformat(), module, _safe_json_dumps(data), quip)
    ) 
    cursor.connection.commit()
#i see what you mean
def cleanup(cursor):
    """Remove entries older than 30 days to prevent database bloat."""
    cutoff_time = time.time() - (30 * 24 * 60 * 60) 
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
            str(raw_value),  
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
    canonical_username = _canonical_username(username)
    cursor.execute(
        """
        SELECT id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count
        FROM sessions WHERE LOWER(username) = ?
        """,
        (canonical_username,)
    )
    row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'username': row[1],
            'persona': row[2],
            'closeness': row[3],
            'slip_intensity': row[4],
            'created_at': row[5],
            'last_accessed': row[6],
            'session_count': row[7]
        }
    return None

def save_session(cursor, session_id, username, persona, closeness, slip_intensity):
    """Save or update session state. Called at session end."""
    current_time = time.time()
    canonical_username = _canonical_username(username)
    # Keep a stable per-user row id so users do not collide on the primary key.
    row_id = f"{session_id}:{canonical_username}"
    
    # Try to update existing
    cursor.execute(
        """
        UPDATE sessions 
        SET persona = ?, closeness = ?, slip_intensity = ?, last_accessed = ?, session_count = session_count + 1
        WHERE LOWER(username) = ?
        """,
        (persona, closeness, slip_intensity, current_time, canonical_username)
    )
    
    if cursor.rowcount == 0:
        cursor.execute(
            """
            INSERT INTO sessions (id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (row_id, canonical_username, persona, closeness, slip_intensity, current_time, current_time, 1)
        )
    else:
        
        pass  
    cursor.connection.commit()

def get_quip(cursor, key: str, persona: str) -> str:
    """ #shoudln't this be intheatrics? 
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

def add_quip(cursor, key: str, persona: str, text: str) -> bool: #this is a placeholder,,,no logic yet
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
    

class DatabaseManager:
    def __init__(self, debug=False):
        self.conn, self.cursor = init_db(debug=debug)
        if not self.conn or not self.cursor:
            raise Exception("Failed to initialize database.")

    def close(self):
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None
        self.close = None   
        #halp


    def __enter__(self):
        return self
    #keepyoursecretsthen 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() #thanks
        #soit autosaves? def close is manual.
#he's freaking out right here... #maybe we 
    #so we call __enter__ at the start of the session and __exit__ at the end to ensure proper cleanup and saving.