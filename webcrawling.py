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
class WebCrawler:
    def __init__(self, consent_form):
        self.consent_form = consent_form
        self.consent_given = consent_form.consent_given
        self.out_of_scope_items = {
            item.strip().lower() for item in (consent_form.out_of_scope_items or []) if item.strip()
        }
    def _is_out_of_scope(self, data_type: str) -> bool:
        return data_type.strip().lower() in self.out_of_scope_items #this doesn't work btw. 
    def _is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    def _fetch_page(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching {url}: {e}")
            return ""
    def _extract_links(self, html: str, base_url: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(base_url, href)
            if self._is_valid_url(full_url):
                links.add(full_url)
        return list(links)
    
    def address_bar(self, conn, cursor, session_id, me, autosave=None):
            if not self.consent_given:
                return []
            if self._is_out_of_scope("web crawling"):
                return []
            url = input("Enter a URL to crawl: ").strip()
            if not self._is_valid_url(url):
                print("Invalid URL. Please enter a valid URL.")
                return []
            html = self._fetch_page(url)
            if not html:
                print("Failed to retrieve the page. Please try again.")
                return []
            links = self._extract_links(html, url)
            print(f"Found {len(links)} links on the page.")
            for link in links:
                print(link)
            return links
    def collect_and_log(self, cursor, session_id, me, autosave=None):
        """Compatibility wrapper; orchestration now owns logging and narration."""
        links = self.address_bar(cursor, session_id, me, autosave)

        return links