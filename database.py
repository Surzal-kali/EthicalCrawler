import sqlite3
import json
import random
from datetime import datetime
import os
import time
from pathlib import Path
import re
    # # from reportcard import ReportCard
    # from webcrawling import WebCrawler 
from autosave import AutosaveManager
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, dev_comment, clear
from consentform import ConsentKey
from quips import get_catalog_quip, iter_catalog_quips

def get_evidence_dir() -> Path:
    """Return the project-scoped data directory used for runtime artifacts."""
    configured = os.getenv("ETHICAL_CRAWLER_DATA_DIR", "").strip()
    if configured:
        data_dir = Path(configured).expanduser()
    else:
        data_dir = Path(__file__).resolve().parent / "data"

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_session_state_dir() -> Path:
    """Directory where per-user JSON session state is stored."""
    state_dir = get_evidence_dir() / "session_states"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def _safe_username_slug(username: str) -> str:
    canonical = _canonical_username(username)
    slug = re.sub(r"[^a-z0-9._-]", "_", canonical)
    return slug or "anonymous"


def _session_state_path(username: str) -> Path:
    return get_session_state_dir() / f"{_safe_username_slug(username)}.json"


DATABASE_PATH = get_evidence_dir() / "db" / "li_evidence.db"
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
    # if isinstance(value, ReportCard):
    #     return {
    #         "session_id": value.session_id,
    #         "persona": value.persona,
    #         "services_used": value.services_used,
    #         "data_collected": value.data_collected,
    #         "timestamp": value.timestamp,
    #     } 
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, Exception):
        return f"{type(value).__name__}: {str(value)}" #good catch
    return str(value)


def _safe_json_dumps(data):
    return json.dumps(data, default=_json_default)


def _canonical_username(username: str) -> str:
    """Normalize usernames so session lookup/save is case-insensitive."""
    return (username or "").strip().lower()

canonical_username = _canonical_username


def seed_default_quips(cursor):
    """Seed the quips table with default entries from the catalog if it's empty. takes a database cursor as a parameter. Returns nothing."""
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
    """Initialize the SQLite database, creating tables and seeding data as needed. takes an optional debug flag to enable verbose logging. Returns a tuple of (connection, cursor) if successful, or (None, None) on failure."""
    debug_mode = _debug_enabled(debug)
    conn = None #is it pragma? #
    try:
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('PRAGMA journal_mode=WAL')
        cursor.execute('PRAGMA synchronous=NORMAL')
        cursor.execute('PRAGMA temp_store=MEMORY')
        cursor.execute('''CREATE TABLE IF NOT EXISTS web_links (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT,
                            url TEXT,
                            persona TEXT,
                            context TEXT,
                            timestamp REAL
                        )''')
        cursor.execute ('''
                        CREATE TABLE IF NOT EXISTS reports (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            session_id TEXT,
                            persona TEXT,
                            services_used TEXT,
                            data_collected TEXT,
                            timestamp REAL
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
                user_name TEXT,
                field TEXT,
                raw_value TEXT,
                normalized_key TEXT,
                persona TEXT,
                quip_text TEXT,
                context TEXT,
                timestamp REAL
            )
        ''')
        # Migration: add user_name column to existing logs tables
        try:
            cursor.execute("ALTER TABLE logs ADD COLUMN user_name TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

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
    """Migrate the mood_config table to the latest schema if necessary. This checks for the presence of the 'min_slip' column to determine if migration is needed. If the old schema is detected, the table is dropped and will be recreated with the correct schema on next init. takes a database cursor as a parameter. Returns nothing."""
    cursor.execute("PRAGMA table_info(mood_config)")
    cols = {row[1] for row in cursor.fetchall()}
    # Old schemas lacked min_slip; drop and let init_db recreate with correct schema.
    if cols and 'min_slip' not in cols:
        cursor.execute("DROP TABLE IF EXISTS mood_config")


def _migrate_sessions_usernames(cursor):    
    """Merge legacy mixed-case usernames into a canonical lowercase record. takes a database cursor as a parameter. Returns nothing."""
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
    """Save a piece of evidence to the database with associated metadata. takes database cursor, session_id, module name, data payload, and quip as parameters. Returns nothing."""
    cursor.execute(
        "INSERT INTO evidence (session_id, timestamp, module, data, quip) VALUES (?, ?, ?, ?, ?)",
        (session_id, datetime.now().isoformat(), module, _safe_json_dumps(data), quip)
    ) 
    cursor.connection.commit()
#i see what you mean
def cleanup(cursor):
    """ Perform routine cleanup tasks to prevent database bloat and maintain performance. This includes removing log entries older than 30 days and purging stale session state JSON files. takes a database cursor as a parameter. Returns nothing."""
    """Remove entries older than 30 days to prevent database bloat."""
    cutoff_time = time.time() - (30 * 24 * 60 * 60)
    cursor.execute("DELETE FROM logs WHERE timestamp < ?", (cutoff_time,))
    cursor.connection.commit()
    # Purge stale session state JSON files (sessions live in JSON, not SQLite).
    for state_file in get_session_state_dir().glob("*.json"):
        try:
            data = json.loads(state_file.read_text(encoding="utf-8"))
            if float(data.get("last_accessed", 0)) < cutoff_time:
                state_file.unlink()
        except (json.JSONDecodeError, OSError, ValueError):
            pass
 
def log(cursor, session_id, field, raw_value, narrator, context="system_profiler", normalized_key=None, quip_text=None, user_name=None):
    """Log an interaction or finding to the database with optional normalization and quip generation. takes database cursor, session_id, field name, raw value, narrator object, context string, optional normalized_key, optional quip_text, and optional user_name as parameters. Returns nothing."""
    normalized = normalized_key if normalized_key is not None else narrator.normalize(field, raw_value)
    quip_text = quip_text if quip_text is not None else narrator.quip(field, raw_value, cursor=cursor)
    canonical = _canonical_username(user_name) if user_name else None

    cursor.execute(
        """
        INSERT INTO logs (session_id, user_name, field, raw_value, normalized_key, persona, quip_text, context, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            canonical,
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

def load_session(username: str, cursor=None):
    """Load existing session state by username from JSON, with optional DB fallback."""
    canonical_username = _canonical_username(username)
    state_file = _session_state_path(canonical_username)

    if state_file.exists():
        try:
            payload = json.loads(state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            payload = None

        if isinstance(payload, dict):
            return {
                'id': payload.get('id', f"LI:{canonical_username}"),
                'username': canonical_username,
                'persona': payload.get('persona', 'foothold'),
                'closeness': float(payload.get('closeness', 0)),
                'slip_intensity': float(payload.get('slip_intensity', 5)),
                'created_at': float(payload.get('created_at', time.time())),
                'last_accessed': float(payload.get('last_accessed', time.time())),
                'session_count': int(payload.get('session_count', 1)),
                'consented_at': payload.get('consented_at'),
                'out_of_scope': payload.get('out_of_scope', []),
            }

    # Fallback for older persisted states that still live in SQLite.
    if cursor is None:
        return None

    cursor.execute(
        """
        SELECT id, username, persona, closeness, slip_intensity, created_at, last_accessed, session_count
        FROM sessions WHERE LOWER(username) = ?
        """,
        (canonical_username,)
    )
    row = cursor.fetchone()
    if row:
        session_payload = {
            'id': row[0],
            'username': row[1],
            'persona': row[2],
            'closeness': row[3],
            'slip_intensity': row[4],
            'created_at': row[5],
            'last_accessed': row[6],
            'session_count': row[7]
        }
        try:
            state_file.write_text(json.dumps(session_payload, indent=2), encoding="utf-8")
        except OSError:
            pass
        return session_payload

    return None

def save_session(session_id, username, persona, closeness, slip_intensity, consented_at=None, out_of_scope=None):
    """Save session state to a JSON file for quick loading on next session. takes session_id, username, persona, closeness, slip_intensity, optional consented_at timestamp, and optional out_of_scope list as parameters. Returns nothing."""
    current_time = time.time()
    canonical_username = _canonical_username(username)
    row_id = f"{session_id}:{canonical_username}"
    state_file = _session_state_path(canonical_username)

    previous = None
    if state_file.exists():
        try:
            previous = json.loads(state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            previous = None

    created_at = float(previous.get("created_at", current_time)) if isinstance(previous, dict) else current_time
    prior_count = int(previous.get("session_count", 0)) if isinstance(previous, dict) else 0

    # Preserve consent from first session if not explicitly passed
    if consented_at is None and isinstance(previous, dict):
        consented_at = previous.get("consented_at")
    if out_of_scope is None and isinstance(previous, dict):
        out_of_scope = previous.get("out_of_scope", [])

    from datetime import datetime as _dt
    payload = {
        "id": row_id,
        "username": canonical_username,
        "persona": persona,
        "closeness": float(closeness),
        "slip_intensity": float(slip_intensity),
        "created_at": created_at,
        "created_at_display": _dt.fromtimestamp(created_at).strftime("%d/%m/%y"),
        "last_accessed": current_time,
        "last_accessed_display": _dt.fromtimestamp(current_time).strftime("%d/%m/%y"),
        "session_count": prior_count + 1,
        "consented_at": consented_at,
        "out_of_scope": out_of_scope or [],
    }

    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

def get_quip(cursor, key: str, persona: str) -> str:
    """ 
Retrieve a quip from the database based on key and persona, with fallbacks to 'all' persona and catalog defaults. takes database cursor, quip key, and persona as parameters. Returns the quip text.
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
    """Context manager for database connection handling. Ensures proper initialization and cleanup of the SQLite connection and cursor. takes an optional debug flag to enable verbose logging. Returns a DatabaseManager instance that can be used with 'with' statements."""
    def __init__(self, debug=False):
        self.conn, self.cursor = init_db(debug=debug)
        if not self.conn or not self.cursor:
            raise Exception("Failed to initialize database.")

    def close(self):
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() #good catch