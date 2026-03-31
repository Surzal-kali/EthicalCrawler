import sqlite3
from pathlib import Path
import tempfile

print("Testing DB initialization...")

try:
    temp_dir = Path(tempfile.gettempdir()) / "ethical_crawler"
    temp_dir.mkdir(parents=True, exist_ok=True)
    db_path = temp_dir / "li_evidence.db"
    
    print(f"DB Path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Try creating a simple table
    cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
    conn.commit()
    
    print("✅ Database connection successful!")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Existing tables: {[t[0] for t in tables]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Database error: {e}")