# from webcrawling import WebCrawler
# from enumeration import FileCrawler
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, dev_comment, clear
from services import prog as services_prog
from consentform import ConsentKey
import time
import os
import asyncio
import psutil
import concurrent.futures #so this needs to go
from reportcard import ReportCard, report
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, dev_comment, clear
from consentform import ConsentKey
from database import save_session, load_session, SessionStore
class Digestion:
    """Designed to be the final orchestration of the session summary. It processes the collected data, analyzes it, and prepares it for the report card. This includes analyzing web links collected, files accessed, and eventually shell history to extract insights and patterns. The core logic of digestion would go here, including any necessary computations, data transformations, and summarization for the report card."""
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = consent_form.out_of_scope_items
    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items#wait...maybe we should cut the db? #yeth
    def digest(self, store, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot perform digestion.")
            return None
        if self._is_out_of_scope("digestion"):
            print("Digestion is out of scope. Cannot perform digestion.")
            return None
        if not self.consent_given:
            print("Consent not given. Cannot perform digestion.")
            return None
        if self._is_out_of_scope("digestion"):
            print("Digestion is out of scope. Cannot perform digestion.")
            return None
        
        print("Performing digestion...")
        for field in ["web_links", "files_accessed", "shell_history"]:
            if self._is_out_of_scope(field):
                print(f"{field.replace('_', ' ').title()} is out of scope. Skipping analysis for this field.")
                continue
            print(f"Analyzing {field.replace('_', ' ')}...") 
            time.sleep(1)  # Simulate time taken for analysis
        print("Digestion completed successfully.")
        return {
            "digested_web_links": ["https://example.com", "https://test.com"],
            "digested_files_accessed": ["/path/to/file1.txt", "/path/to/file2.txt"],
            "digested_shell_history": ["ls -la", "cat /etc/passwd"],
        } 