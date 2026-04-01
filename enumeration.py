import sqlite3
import json
import random
from datetime import datetime, timedelta
import os
import time
import tempfile
from pathlib import Path
from theatrics import Me, dev_comment, test, pprint, sudo, equip
from quips import quips
from consentform import ConsentForm
from LIMain import get_evidence_dir, get_db_path

#we could have the user explore their files. and drag and drop what they wanna show off?????

##Persona: foothold, Closeness: 10.0, Slip Intensity: 17.78
# Corrupted Output: CONSENT_UNDERSTANDING—CONSENT_UNDERSTANDING
#he gets it :)
#we need a seperate entity to deal with network logic and browsers. I was gunna have each type of enumeration be a seperate class. But i need all the logic centralized. 
class FileCrawler:
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = consent_form.out_of_scope_items
        self.evidence_dir = get_evidence_dir()
        self.db_path = get_db_path()
        self.slip_intensity = 0
        self.knowledge_base = {}
        self.initialize_db()
    def initialize_db(self):
        try:
            os.makedirs(self.evidence_dir, exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    data_type TEXT,
                    data_content TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
    def collect_evidence(self, data_type, data_content):
        if not self.consent_given:
            print("Consent not given. Cannot collect evidence.")
            return
        if data_type in self.out_of_scope_items:
            print(f"Data type '{data_type}' is out of scope. Skipping collection.")
            return
        timestamp = datetime.now().isoformat()
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO evidence (timestamp, data_type, data_content)
                VALUES (?, ?, ?)
            """, (timestamp, data_type, json.dumps(data_content)))
            conn.commit()
            conn.close()
            self.knowledge_base[data_type] = data_content
            self.slip_intensity += 1
        except Exception as e:
            print(f"❌ Database error: {e}")
            conn.close()
    def get_evidence_dir(self, evidence_dir=None):
        """Get platform-aware evidence directory."""
        if evidence_dir is None:
            base_dir = Path.home() / "ethical_crawler_data"
            evidence_dir = base_dir / "evidence"
            evidence_dir.mkdir(parents=True, exist_ok=True)
            return evidence_dir