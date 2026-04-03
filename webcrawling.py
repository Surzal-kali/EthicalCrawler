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
import json #no
#######please note this is currently dead code, and unimplemented. I want to be elegant in my approach and enumerate as much as possible, and until i can think of an ethical and legal way to do that without breaking my cpu i'll let you know :) also if i call it i can't run it on my kali-pi anymore and that makes me sad :(   
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
    
    def addy_bar(self, conn, cursor, session_id, me, autosave=None):
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
            return links 
    def collect_and_log(self, cursor, session_id, me, autosave=None):
        """Compatibility wrapper; orchestration now owns logging and narration."""
        links = self.addy_bar(cursor, session_id, me, autosave)

        return links

    def user_agent(self, conn, cursor, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot collect user agent.")
            return None
        if self._is_out_of_scope("user agent collection"):
            print("User agent collection is out of scope. Cannot collect user agent.")
            return None
        user_agent = requests.utils.default_user_agent()
        print(f"User Agent: {user_agent}")
        return user_agent #the internet has rules after all lets check for robots.txt next. 
    

    def robots_txt(self, conn, cursor, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot check robots.txt.")
            return None
        if self._is_out_of_scope("robots.txt checking"):
            print("Robots.txt checking is out of scope. Cannot check robots.txt.")
            return None
        url = input("Enter the base URL to check for robots.txt: ").strip()
        if not self._is_valid_url(url):
            print("Invalid URL. Please enter a valid URL.")
            return None
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        try:
            response = requests.get(robots_url, timeout=10)
            if response.status_code == 200:
                print(f"Robots.txt found at {robots_url}:\n{response.text}")
                return response.text
            else:
                print(f"No robots.txt found at {robots_url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error fetching robots.txt from {robots_url}: {e}")
            return None
        
