# from webcrawling import WebCrawler
# from enumeration import FileCrawler
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, dev_comment, clear
from services import prog as services_prog
from consentform import ConsentKey
import time
import os
import asyncio
import psutil
import concurrent.futures
class Digestion:
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
        #hold plz pi is being mean :(  )
        """Designed to be the final orchestration of the session summary. It processes the collected data, analyzes it, and prepares it for the report card. This includes analyzing web links collected, files accessed, and shell history to extract insights and patterns. The core logic of digestion would go here, including any necessary computations, data transformations, and summarization for the report card."""
        if not self.consent_given:
            print("Consent not given. Cannot perform digestion.")
            return None
        if self._is_out_of_scope("digestion"):
            print("Digestion is out of scope. Cannot perform digestion.")
            return None
        
        print("Performing digestion...")
        # Here we would process the collected data, analyze it, and prepare it for the report card.
        # For example, we could analyze the web links collected, the files accessed, and the shell history to extract insights and patterns.
        # This is where the core logic of digestion would go, including any necessary computations, data
        # transformations, and summarization for the report card.
        print("Digestion completed successfully.")