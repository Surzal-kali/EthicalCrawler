import csv
from importlib.resources import files
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from enumeration import FileCrawler #this is so hacky but it works for now, we can refactor later to be more elegant and less tightly coupled. #yeth

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
    canonical = canonical_username(username)
    slug = re.sub(r"[^a-z0-9._-]", "_", canonical)
    return slug or "anonymous"


def _session_state_path(username: str) -> Path:
    return get_session_state_dir() / f"{_safe_username_slug(username)}.json"


DATABASE_PATH = get_evidence_dir() / "db" / "li_evidence.db"  # legacy path, kept for migration reference only


def _json_default(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (set, tuple)):
        return list(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, Exception):
        return f"{type(value).__name__}: {str(value)}"
    return str(value)


def _safe_json_dumps(data):
    return json.dumps(data, default=_json_default)


def canonical_username(username: str) -> str:
    """Normalize usernames so session lookup/save is case-insensitive."""
    return (username or "").strip().lower()


canonical_username = canonical_username


# ---------------------------------------------------------------------------
# SessionStore — in-memory session state with real-time CSV audit logging
# ---------------------------------------------------------------------------

_CSV_FIELDNAMES = [
    "timestamp", "session_id", "user_name", "field",
    "raw_value", "normalized_key", "persona", "quip_text", "context",
]


class SessionStore:
    """
    Replaces the SQLite layer entirely.
    Holds in-memory state for the session and streams log entries to a per-user CSV file.
    Pass this object through the call stack instead of (conn, cursor).
    """

    def __init__(self, session_id: str, user_name: str):
        self.session_id = session_id
        self.user_name = canonical_username(user_name)
        self._log_entries: list = []
        self._services_seen: set = set()
        #this is so clean.... elegant...not sql at all. i hate sql. so much. we can feed it to so many end points! 
        log_dir = get_evidence_dir() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        slug = _safe_username_slug(user_name)#
        self._csv_path = log_dir / f"{slug}.csv"

        new_file = not self._csv_path.exists()
        self._csv_file = self._csv_path.open("a", newline="", encoding="utf-8")
        self._csv_writer = csv.DictWriter(self._csv_file, fieldnames=_CSV_FIELDNAMES)
        if new_file:
            self._csv_writer.writeheader()
            self._csv_file.flush()

    def add_log(
        self,
        field: str,
        value: Any,
        context: Optional[str] = None,
        persona: Optional[str] = None,
        normalized_key: Optional[str] = None,
        quip_text: Optional[str] = None,
        user_name: Optional[str] = None,
    ) -> None:

        """Write one log entry to CSV and keep an in-memory mirror."""
        try:
            raw_str = json.dumps(value, default=_json_default)
        except Exception:
            raw_str = str(value)
        row = {
            "timestamp": time.time(),
            "session_id": self.session_id,
            "user_name": user_name or self.user_name,
            "field": field,
            "raw_value": raw_str,
            "normalized_key": normalized_key or "",
            "persona": persona or "",
            "quip_text": quip_text or "",
            "context": context or "",
        }
        self._log_entries.append(row)
        try:
            self._csv_writer.writerow(row)
            self._csv_file.flush()
        except Exception:
            pass  # in-memory entry still captured even if disk write fails

    def get_log(self) -> list:
        """Return in-memory log entries for display (e.g. goodbye summary)."""
        return list(self._log_entries)

    def add_service(self, name: str) -> bool:
        """Register a detected service. Returns True if new, False if already seen."""
        key = name.strip().lower()
        if key in self._services_seen:
            return False
        self._services_seen.add(key)
        return True

    def close(self) -> None:
        """Flush and close the CSV file handle."""
        try:
            self._csv_file.flush()
            self._csv_file.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Session state (JSON persistence)
# ---------------------------------------------------------------------------

def load_session(username: str):
    """Load existing session state by username from JSON."""
    canonical = canonical_username(username)
    state_file = _session_state_path(canonical)

    if state_file.exists():
        try:
            payload = json.loads(state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            payload = None

        if isinstance(payload, dict):
            return {
                'id': payload.get('id', f"LI:{canonical}"),
                'username': canonical,
                'persona': payload.get('persona', 'foothold'),
                'closeness': float(payload.get('closeness', 0)),
                'slip_intensity': float(payload.get('slip_intensity', 5)),
                'created_at': float(payload.get('created_at', time.time())),
                'last_accessed': float(payload.get('last_accessed', time.time())),
                'session_count': int(payload.get('session_count', 1)),
                'consented_at': payload.get('consented_at'),
                'out_of_scope': payload.get('out_of_scope', []),
            }

    return None

def save_session(session_id, username, persona, closeness, slip_intensity, consented_at=None, out_of_scope=None, report_card=None):
    """Save session state to a JSON file for quick loading on next session. takes session_id, username, persona, closeness, slip_intensity, optional consented_at timestamp, optional out_of_scope list, and optional report_card dictionary as parameters. Returns nothing."""
    current_time = time.time()
    canonical = canonical_username(username)
    row_id = f"{session_id}:{canonical}"
    state_file = _session_state_path(canonical)

    previous = None
    if state_file.exists():
        try:
            previous = json.loads(state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            previous = None

    created_at = float(previous.get("created_at", current_time)) if isinstance(previous, dict) else current_time
    prior_count = int(previous.get("session_count", 0)) if isinstance(previous, dict) else 0


    if consented_at is None and isinstance(previous, dict):
        consented_at = previous.get("consented_at")
    if out_of_scope is None and isinstance(previous, dict):
        out_of_scope = previous.get("out_of_scope", [])

    from datetime import datetime as _dt
    payload = {
        "id": row_id,
        "username": canonical,
        "persona": persona,
        "closeness": float(closeness),
        "slip_intensity": float(slip_intensity),
        "created_at": created_at,
        "created_at_display": _dt.fromtimestamp(created_at).strftime("%d/%m/%y"),
        "last_accessed": current_time,
        "last_accessed_display": _dt.fromtimestamp(current_time).strftime("%d/%m/%y"),
        "session_count": prior_count + 1,
        "consented_at": consented_at,
        "out_of_scope": out_of_scope,
        "reportcard": report_card or {},
        "user_name": canonical,
        "enumeration": {
            "files_collected": False,
            "services_detected": 0,
        },
        "crawling": {
            "pages_crawled": 0,
            "data_points_collected": 0,
        },
        "compliance_score": None,
    }
    state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# （づ￣3￣）づ╭❤️～ #