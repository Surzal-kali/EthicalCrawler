
"""
Autosave Manager — buffered persistence with error recovery.
Pass instance through function calls to accumulate and save incrementally.
Supports partial saves: successful fields persist even if others fail.
"""

import sqlite3
import json
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple


class AutosaveManager:
    """
    Buffers collected data and manages persistence with error handling.
    
    Use by:
    1. Create: autosave = AutosaveManager(cursor, session_id, narrator=me)
    2. Collect: autosave.add("field_name", value, context="source_info")
    3. Pass: carry through function calls
    4. Flush: status = autosave.flush(allow_partial=True)
    5. Retry: if status["failed"], autosave.retry_failed()
    """
    
    def __init__(self, cursor: sqlite3.Cursor, session_id: str, narrator=None):
        """
        Initialize autosave manager.
        
        Args:
            cursor: SQLite cursor (from database.init_db())
            session_id: Session identifier (e.g., "LI")
            narrator: Optional Me instance for logging commentary
        """
        self.cursor = cursor
        self.session_id = session_id
        self.narrator = narrator
        self.buffer: Dict[str, Dict[str, Any]] = {}  # field -> {value, context}
        self.failed_fields: Dict[str, str] = {}  # field -> error_reason
        self.failed_payloads: Dict[str, Dict[str, Any]] = {}  # field -> original buffered data
        self.saved_count = 0
        self.flush_count = 0
        
    def add(self, field: str, value: Any, context: str = None) -> bool:
        """
        Buffer a data point. Returns False if field already in buffer.
        
        Args:
            field: Field name/identifier
            value: Data to save (will be JSON serialized)
            context: Optional metadata (e.g., "enumeration_stage", "service_discovery")
        
        Returns:
            True if added, False if field already exists in buffer
        """
        if field in self.buffer:
            return False
        
        self.buffer[field] = {
            "value": value,
            "context": context,
            "timestamp": time.time()
        }
        return True
    
    def _serialize_value(self, value: Any) -> str:
        """Helper: safely serialize value to JSON."""
        try:
            return json.dumps(value, default=str)
        except Exception:
            return json.dumps({"_serialization_error": str(value)})
    
    def flush(self, allow_partial: bool = True) -> Dict[str, List[str]]:
        """
        Persist buffered data. Returns status report.
        
        Args:
            allow_partial: If True, saves successful fields even if some fail.
                          If False, raises on first error (atomic behavior).
        
        Returns:
            {"saved": [fields], "failed": [fields]}
        """
        results = {"saved": [], "failed": []}
        
        if not self.buffer:
            self.flush_count += 1
            return results
        
        for field, data in list(self.buffer.items()):
            try:
                self.cursor.execute("""
                    INSERT INTO logs (session_id, field, raw_value, normalized_key, persona, quip_text, context, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.session_id,
                    field,
                    self._serialize_value(data["value"]),
                    None,  # normalized_key - not tracked in autosave
                    self.narrator.persona if self.narrator else None,
                    None,  # quip_text - not stored here
                    data.get("context"),
                    data.get("timestamp", time.time())
                ))
                results["saved"].append(field)
                self.saved_count += 1
                del self.buffer[field]  # Only remove if successful
                self.failed_fields.pop(field, None)
                self.failed_payloads.pop(field, None)
                
            except Exception as e:
                error_msg = f"{type(e).__name__}: {str(e)}"
                
                if not allow_partial:
                    raise RuntimeError(
                        f"Autosave failed on field '{field}' — {error_msg}\n"
                        f"Saved so far: {results['saved']}"
                    ) from e
                
                self.failed_fields[field] = error_msg
                self.failed_payloads[field] = data.copy()
                results["failed"].append(field)
        
        # Commit successful saves
        if results["saved"]:
            try:
                self.cursor.connection.commit()
            except Exception:
                pass  # Connection may handle commits automatically
        
        self.flush_count += 1
        return results
    
    def retry_failed(self) -> Dict[str, List[str]]:
        """
        Attempt to save previously failed fields again.
        
        Returns:
            {"saved": [fields], "failed": [fields]} (fresh attempt)
        """
        if not self.failed_fields:
            return {"saved": [], "failed": []}
        
        # Move failed fields back to buffer
        for field, _ in self.failed_fields.items():
            if field not in self.buffer:
                payload = self.failed_payloads.get(field)
                if payload is not None:
                    self.buffer[field] = payload.copy()
        
        self.failed_fields.clear()
        self.failed_payloads.clear()
        return self.flush(allow_partial=True)
    
    def peek_buffer(self) -> Dict[str, Dict[str, Any]]:
        """Inspect buffered data without flushing."""
        return self.buffer.copy()
    
    def peek_failed(self) -> Dict[str, str]:
        """Inspect failed fields and their error reasons."""
        return self.failed_fields.copy()
    
    def summary(self) -> Dict[str, Any]:
        """Get current state summary."""
        return {
            "buffered": len(self.buffer),
            "failed": len(self.failed_fields),
            "saved_total": self.saved_count,
            "flush_count": self.flush_count
        }
    
    def clear(self):
        """Clear all buffers (destructive; use with caution)."""

        self.buffer.clear()
        self.failed_fields.clear()
        self.failed_payloads.clear()
class AutosaveCheckpoint:
    """
    Lightweight checkpoint: save state and restore on error recovery.
    Useful for multi-stage pipelines where you want to know what was attempted.
    """
    
    def __init__(self, autosave: AutosaveManager):
        self.autosave = autosave
        self.checkpoint_state = None
    
    def mark(self):
        """Snapshot current state before risky operation."""
        self.checkpoint_state = {
            "buffer": self.autosave.buffer.copy(),
            "failed": self.autosave.failed_fields.copy(),
            "saved_count": self.autosave.saved_count
        }
    
    def rollback(self):
        """Restore to marked checkpoint."""
        if self.checkpoint_state is None:
            raise RuntimeError("No checkpoint marked")
        
        self.autosave.buffer = self.checkpoint_state["buffer"].copy()
        self.autosave.failed_fields = self.checkpoint_state["failed"].copy()
        self.autosave.saved_count = self.checkpoint_state["saved_count"]
