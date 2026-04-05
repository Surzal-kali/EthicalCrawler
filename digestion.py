from webcrawling import WebCrawler
from enumeration import FileCrawler
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
import json
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
            for log_entry in store.get_log():
                if log_entry["context"] == "web_crawling" and field == "web_links":
                    from urllib.parse import urlparse
                    log_entry_links = log_entry.get("value", [])
                    analyzed_links = []
                    for link in log_entry_links:
                        parsed_link = urlparse(link)
                        analyzed_links.append({
                            "url": link,
                            "domain": parsed_link.netloc,
                            "path": parsed_link.path,
                            "scheme": parsed_link.scheme,
                            "is_external": parsed_link.netloc != urlparse(log_entry.get("base_url", "")).netloc,
                            "is_secure": parsed_link.scheme == "https",
                        })
                    for link in analyzed_links:
                        store.add_log_entry({
                            "session_id": session_id,
                            "context": "digestion",
                            "field": "web_links",
                            "value": analyzed_links,
                            "timestamp": time.time(),
                        })
                    analyzed_links = log_entry.get("value", [])
                    return {
                        "digested_web_links": analyzed_links, #insert web links here],
                    }
                elif log_entry["context"] == "enumeration" and field == "files_accessed":
                    for file in log_entry.get("value", []):
                        store.add_log_entry({
                            "session_id": session_id,
                            "context": "digestion",
                            "field": "files_accessed",
                            "value": {
                                "file_path": file.get("enumeration_file_path"),
                                "file_name": file.get("enumeration_file_name"),
                                "file_extension": file.get("enumeration_file_extension"),
                                "file_size_bytes": file.get("enumeration_file_size_bytes"),
                                "file_type": file.get("enumeration_file_type"),
                                "file_preview": file.get("enumeration_file_preview"),
                            },
                            "timestamp": time.time(),
                        })
                    files_accessed = log_entry.get("value", [])
                    return {
                        "digested_files_accessed": files_accessed
                    }
                # elif log_entry["context"] == "shell_history" and field == "shell_history":
                #     # Analyze shell history and extract insights
                #     pass  # Placeholder for actual analysis logic

        return {
            "digested_web_links": [], #insert web links here],
            "digested_files_accessed": [] #insert files accessed here],
        }

#lets just read from the csv since it auto updates and then we can pass the digested insights to the report card for narration. #yeth