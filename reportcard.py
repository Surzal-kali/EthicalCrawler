from database import DatabaseManager
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, dev_comment, clear
from services import prog as services_prog
from consentform import ConsentKey
import time
from bs4 import BeautifulSoup
import requests
import threading
import pdfkit
import re
import tkinter as tk
from tkinter import filedialog
import psutil
from pathlib import Path
from urllib.parse import urlparse, urljoin
import os
class ReportCard: 
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = consent_form.out_of_scope_items
    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items
    def generate(self, cursor, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot generate report card.")
            return {}
        if self._is_out_of_scope("report card"):
            print("Report card generation is out of scope. Cannot generate report card.")
            return {}
        # Placeholder for actual report card generation logic
        report_card = {
            "session_id": session_id,
            "persona": me.persona,
            "services_used": services_prog.services_used,
            "data_collected": {
                "web_links": [],  # This would be populated with actual data
                "files": [],      # This would be populated with actual data
                "shell_history": []  # This would be populated with actual data
            },
            "timestamp": time.time()
        }
        print("Report card generated successfully.")
        return report_card