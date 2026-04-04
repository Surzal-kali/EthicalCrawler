
from theatrics import Me, dev_comment, speak, test, sudo, equip, slip_trigger, clear
from consentform import ConsentKey
import time
from bs4 import BeautifulSoup
import requests
import threading
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import psutil
from pathlib import Path
from urllib.parse import urlparse, urljoin
import os
import json
import datetime
import concurrent.futures

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
     #addy bar is kind of the main event. mood drives everything now.

    def _crawl_config(self, me):
        """Map Me's current state to crawl aggressiveness."""
        if me.persona == "sudo" or me.slip_intensity >= 10:
            return {"threads": "high", "concurrency": 5, "rate": 5}
        elif me.persona == "helper" or me.closeness >= 50:
            return {"threads": "medium", "concurrency": 3, "rate": 3}
        elif me.persona == "foothold" or me.closeness >= 20:
            return {"threads": "low", "concurrency": 1, "rate": 1}
        else:
            return {"threads": "stop", "concurrency": 0, "rate": 0}

    def addy_bar(self, store, session_id, me, autosave=None):
        if not self.consent_given:
            speak(me, "You haven't said yes. I'm not going anywhere.")
            return []

        if self._is_out_of_scope("web"):
            speak(me, "Web's off the table. You said so yourself.")
            return []

        config = self._crawl_config(me)
        if config["threads"] == "stop":
            speak(me, "Not today. The network stays quiet.")
            return []

        root = tk.Tk()
        root.withdraw()
        url = simpledialog.askstring("Web Crawler", "Enter the URL to crawl:")
        root.destroy()

        if not url:
            speak(me, "No address. Nothing to chase.")
            return []
        if not self._is_valid_url(url):
            speak(me, "That's not a real place. Try again.")
            return []

        speak(me, f"Reaching out to {url}... [{config['threads']} intensity]")
        html = self._fetch_page(url)
        if not html:
            speak(me, "Nothing came back. The page isn't talking.")
            return []

        links = self._extract_links(html, url)
        store.add_log("web_crawl_base", url, context="webcrawler", persona=me.persona)

        def fetch_and_log(link):
            time.sleep(1 / config["rate"])
            self._fetch_page(link)
            store.add_log("web_link", link, context="webcrawler", persona=me.persona)

        with concurrent.futures.ThreadPoolExecutor(max_workers=config["concurrency"]) as executor:
            executor.map(fetch_and_log, links)

        speak(me, f"Found {len(links)} links. All accounted for.")
        return links
    
    def collect_and_log(self, store, session_id, me, autosave=None):
        """Compatibility wrapper; orchestration now owns logging and narration."""
        links = self.addy_bar(store, session_id, me, autosave)

        return links

    def user_agent(self, store, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot collect user agent.")
            return None
        if self._is_out_of_scope("user agent collection"):
            print("User agent collection is out of scope. Cannot collect user agent.")
            return None
        user_agent = requests.utils.default_user_agent()
        print(f"User Agent: {user_agent}")
        return user_agent #the internet has rules after all lets check for robots.txt next. 
    

    def robots_txt(self, store, session_id, me, autosave=None):
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
def web_payload(): #but payload makes it sound cool and important, so maybe we keep it? #yeth
    consent_form = ConsentKey()
    consent_form.display()
    consent_data = consent_form.get_consent()
    useragaent = WebCrawler(consent_form).user_agent(None, None, None)
    robotstxt = WebCrawler(consent_form).robots_txt(None, None, None)
    return {
        "consent_data": consent_data,
        "user_agent": useragaent,
        "robots_txt": robotstxt
    }


    print(consent_data)

