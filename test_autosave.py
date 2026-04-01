"""
Test suite for autosave.py — buffering, persistence, and error recovery.
Run with: python test_autosave.py
"""

import sqlite3
import json
import sys
import os
from pathlib import Path

# Add parent to path so we can import autosave
sys.path.insert(0, str(Path(__file__).parent))

from autosave import AutosaveManager, AutosaveCheckpoint


def setup_test_db():
    """Create in-memory SQLite database with logs table."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            field TEXT,
            raw_value TEXT,
            context TEXT,
            timestamp REAL
        )
    ''')
    conn.commit()
    return conn, cursor


def test_basic_add_and_flush():
    """Test: Buffer and flush simple data."""
    print("\n[TEST 1] Basic add and flush...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_1")
    
    # Add some data
    assert autosave.add("hostname", "attacker-pc", context="enumeration") == True
    assert autosave.add("os_type", "Windows", context="enumeration") == True
    assert len(autosave.buffer) == 2
    
    # Flush
    status = autosave.flush()
    assert len(status["saved"]) == 2
    assert status["saved"] == ["hostname", "os_type"]
    assert len(status["failed"]) == 0
    assert autosave.saved_count == 2
    assert len(autosave.buffer) == 0
    
    # Verify persistence
    cursor.execute("SELECT field, raw_value FROM logs WHERE session_id = ?", ("test_session_1",))
    rows = cursor.fetchall()
    assert len(rows) == 2
    
    print("  ✓ Added 2 fields, flushed, verified in database")
    conn.close()


def test_duplicate_add_rejected():
    """Test: Cannot add same field twice."""
    print("\n[TEST 2] Duplicate add rejection...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_2")
    
    # First add succeeds
    assert autosave.add("service", "ssh", context="discovery") == True
    
    # Second add with same field fails
    assert autosave.add("service", "http", context="discovery") == False
    assert len(autosave.buffer) == 1
    assert autosave.buffer["service"]["value"] == "ssh"  # Original preserved
    
    print("  ✓ Duplicate add correctly rejected")
    conn.close()


def test_partial_saves():
    """Test: Successful fields persist even if some fail."""
    print("\n[TEST 3] Partial saves (allow_partial=True)...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_3")
    
    # Add valid data
    autosave.add("valid_field_1", "data1", context="stage1")
    autosave.add("valid_field_2", "data2", context="stage1")
    
    # Flush with partial=True
    status = autosave.flush(allow_partial=True)
    assert len(status["saved"]) == 2
    assert len(status["failed"]) == 0
    assert autosave.saved_count == 2
    
    # Verify all saved
    cursor.execute("SELECT COUNT(*) FROM logs WHERE session_id = ?", ("test_session_3",))
    count = cursor.fetchone()[0]
    assert count == 2
    
    print("  ✓ All fields saved successfully")
    conn.close()


def test_serialization_edge_cases():
    """Test: Complex types serialize safely."""
    print("\n[TEST 4] Serialization edge cases...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_4")
    
    # Complex types
    autosave.add("dict_data", {"nested": {"key": "value"}, "ports": [22, 80, 443]})
    autosave.add("list_data", [1, 2, 3, "mixed", None])
    autosave.add("none_data", None)
    autosave.add("special_chars", "with\nnewlines\tand\ttabs")
    
    status = autosave.flush()
    assert len(status["saved"]) == 4
    assert autosave.saved_count == 4
    
    # Verify retrieval
    cursor.execute("SELECT raw_value FROM logs WHERE field = ? AND session_id = ?", 
                   ("dict_data", "test_session_4"))
    raw = cursor.fetchone()[0]
    parsed = json.loads(raw)
    assert parsed["nested"]["key"] == "value"
    assert parsed["ports"] == [22, 80, 443]
    
    print("  ✓ Complex types serialized and persisted correctly")
    conn.close()


def test_context_tracking():
    """Test: Context metadata preserved."""
    print("\n[TEST 5] Context tracking...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_5")
    
    autosave.add("field_a", "val_a", context="enumeration_stage")
    autosave.add("field_b", "val_b", context="service_discovery")
    
    status = autosave.flush()
    assert len(status["saved"]) == 2
    
    # Verify context stored
    cursor.execute("SELECT field, context FROM logs WHERE session_id = ?", 
                   ("test_session_5",))
    rows = cursor.fetchall()
    contexts = {row[0]: row[1] for row in rows}
    assert contexts["field_a"] == "enumeration_stage"
    assert contexts["field_b"] == "service_discovery"
    
    print("  ✓ Context metadata preserved in database")
    conn.close()


def test_peek_methods():
    """Test: Inspect buffer without modifying."""
    print("\n[TEST 6] Peek methods...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_6")
    
    autosave.add("field1", "value1")
    autosave.add("field2", "value2")
    
    # Peek at buffer
    buffer = autosave.peek_buffer()
    assert len(buffer) == 2
    assert buffer["field1"]["value"] == "value1"
    
    # Peek at failed (should be empty)
    failed = autosave.peek_failed()
    assert len(failed) == 0
    
    # Peek doesn't modify
    assert len(autosave.buffer) == 2
    
    print("  ✓ Peek methods work without side effects")
    conn.close()


def test_summary():
    """Test: Summary reports current state."""
    print("\n[TEST 7] Summary state reporting...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_7")
    
    autosave.add("f1", "v1")
    autosave.add("f2", "v2")
    
    summary = autosave.summary()
    assert summary["buffered"] == 2
    assert summary["failed"] == 0
    assert summary["saved_total"] == 0
    assert summary["flush_count"] == 0
    
    autosave.flush()
    summary = autosave.summary()
    assert summary["buffered"] == 0
    assert summary["saved_total"] == 2
    assert summary["flush_count"] == 1
    
    print("  ✓ Summary accurately reflects state")
    conn.close()


def test_multiple_flushes():
    """Test: Multiple flush cycles."""
    print("\n[TEST 8] Multiple flush cycles...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_8")
    
    # First batch
    autosave.add("batch1_field1", "data1")
    autosave.add("batch1_field2", "data2")
    status1 = autosave.flush()
    assert len(status1["saved"]) == 2
    assert autosave.saved_count == 2
    
    # Second batch
    autosave.add("batch2_field1", "data3")
    status2 = autosave.flush()
    assert len(status2["saved"]) == 1
    assert autosave.saved_count == 3
    
    # Verify all 3 in database
    cursor.execute("SELECT COUNT(*) FROM logs WHERE session_id = ?", ("test_session_8",))
    count = cursor.fetchone()[0]
    assert count == 3
    
    print("  ✓ Multiple flush cycles work correctly")
    conn.close()


def test_empty_flush():
    """Test: Flush with empty buffer."""
    print("\n[TEST 9] Empty buffer flush...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_9")
    
    # Flush empty
    status = autosave.flush()
    assert status == {"saved": [], "failed": []}
    assert autosave.flush_count == 1  # Still increments
    
    print("  ✓ Empty buffer flush handled gracefully")
    conn.close()


def test_checkpoint_mark_and_rollback():
    """Test: Checkpoint save and restore."""
    print("\n[TEST 10] Checkpoint mark and rollback...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_10")
    checkpoint = AutosaveCheckpoint(autosave)
    
    # Add some data
    autosave.add("field1", "value1")
    autosave.add("field2", "value2")
    autosave.flush()
    
    # Mark checkpoint
    checkpoint.mark()
    assert checkpoint.checkpoint_state is not None
    assert checkpoint.checkpoint_state["saved_count"] == 2
    
    # Add more data
    autosave.add("field3", "value3")
    autosave.add("field4", "value4")
    assert len(autosave.buffer) == 2
    
    # Rollback to checkpoint
    checkpoint.rollback()
    assert len(autosave.buffer) == 0
    assert autosave.saved_count == 2
    
    print("  ✓ Checkpoint mark and rollback work correctly")
    conn.close()


def test_clear():
    """Test: Clear all buffers."""
    print("\n[TEST 11] Clear buffers...")
    conn, cursor = setup_test_db()
    autosave = AutosaveManager(cursor, "test_session_11")
    
    autosave.add("f1", "v1")
    autosave.add("f2", "v2")
    assert len(autosave.buffer) == 2
    
    autosave.clear()
    assert len(autosave.buffer) == 0
    assert autosave.saved_count == 0  # Does not affect saved_count
    
    print("  ✓ Clear buffers work correctly")
    conn.close()


def test_retry_failed_preserves_original_payload():
    """Test: retry_failed keeps original value/context instead of writing nulls."""
    print("\n[TEST 12] Retry failed preserves original payload...")
    conn, real_cursor = setup_test_db()

    class FaultyCursor:
        def __init__(self, cursor):
            self._cursor = cursor
            self._failed_once = False

        def execute(self, sql, params=None):
            if params is not None and sql.strip().startswith("INSERT INTO logs"):
                field = params[1]
                if field == "retry_field" and not self._failed_once:
                    self._failed_once = True
                    raise sqlite3.OperationalError("simulated transient write failure")
            if params is None:
                return self._cursor.execute(sql)
            return self._cursor.execute(sql, params)

    autosave = AutosaveManager(FaultyCursor(real_cursor), "test_session_12")

    autosave.add("retry_field", {"k": "v"}, context="retry_context")
    status = autosave.flush(allow_partial=True)
    assert status["failed"] == ["retry_field"]

    retry_status = autosave.retry_failed()
    assert retry_status["saved"] == ["retry_field"]
    assert retry_status["failed"] == []

    real_cursor.execute(
        "SELECT raw_value, context FROM logs WHERE session_id = ? AND field = ?",
        ("test_session_12", "retry_field"),
    )
    row = real_cursor.fetchone()
    assert row is not None
    assert json.loads(row[0]) == {"k": "v"}
    assert row[1] == "retry_context"

    print("  ✓ Failed retries keep original payload and context")
    conn.close()


def run_all_tests():
    """Execute all tests."""
    print("\n" + "="*60)
    print("AUTOSAVE MODULE TEST SUITE")
    print("="*60)
    
    tests = [
        test_basic_add_and_flush,
        test_duplicate_add_rejected,
        test_partial_saves,
        test_serialization_edge_cases,
        test_context_tracking,
        test_peek_methods,
        test_summary,
        test_multiple_flushes,
        test_empty_flush,
        test_checkpoint_mark_and_rollback,
        test_clear,
        test_retry_failed_preserves_original_payload,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
