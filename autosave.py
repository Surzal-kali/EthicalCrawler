
"""
Autosave Manager — buffered persistence with error recovery.
Pass instance through function calls to accumulate and save incrementally.
Supports partial saves: successful fields persist even if others fail.
"""

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
    
    def __init__(self, store, session_id: str, narrator=None, user_name: str = None):
        """
        Initialize autosave manager.
        
        Args:
            store: SessionStore instance (from database.SessionStore)
            session_id: Session identifier (e.g., "LI")
            narrator: Optional Me instance for logging commentary
            user_name: Optional username for per-user log filtering
        """
        self.store = store
        self.session_id = session_id
        self.narrator = narrator
        self.user_name = (user_name or "").strip().lower() or None
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
                self.store.add_log(
                    field,
                    data["value"],
                    context=data.get("context"),
                    persona=self.narrator.persona if self.narrator else None,
                )
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
        decode_quip = lambda x: x #ok explain lambda cause my teacher never tuaght me :( ) # we have the logic in quips tho don't worry it's just a placeholder here. #yeth (❁´◡`❁)
        decoded_buffer = {}
        for field, data in self.buffer.items():
            decoded_data = data.copy()
            if "quip_text" in decoded_data:
                decoded_data["quip_text"] = decode_quip(decoded_data["quip_text"], {}, None)
            decoded_buffer[field] = decoded_data
        return decoded_buffer
    
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
