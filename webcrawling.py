
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
import json 
import datetime
import threading
import concurrent.futures
import pdfkit
import re
import asyncio #unsure but sounds good. #
from tkinter import simpledialog
from tkinter import messagebox



#am i missing anything? #
#######current problems, it needs some form of background slowdown while crawling, and we need to wire it into chattin in a way that feels organic, and allows us to pick up keywords during the main orchestration.


# Web crawling logic
# take url, split into base and path, check robots.txt, crawl allowed pages, extract links, log the tree and snapshot the required padges into pdfs. also collect user agent and other metadata. needs to be careful about rate limiting and not crashing the system. should be able to exclude web crawling from the scope if the user chooses. we also need concurrency and rate limiting. we can use threading or asyncio for concurrency, and we can implement a simple rate limiter to avoid overwhelming the system or the target website. we also need to handle errors gracefully and log them for the report card. we are bothering people other than the user, so extra logging is needed. need to make sure everythign works properly on web server connection and crawl. 



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
     #addy bar is kind of the main event and is very basic rn. #report card is at the end of the sprint shhhhhhhhhhhh


    def addy_bar(self, cursor, session_id, me, autosave=None):
        if not self.consent_given:
            print("Consent not given. Cannot perform web crawling.")
            return []


        elif self._is_out_of_scope("web crawling"):
            print("Web crawling is out of scope. Cannot perform web crawling.")
            return []

        else:
            import tk as tk
            from tkinter import simpledialog
            root = tk.Tk()
            root.withdraw()
            url = simpledialog.askstring("Web Crawler", "Enter the URL to crawl:")
            if not url:
                print("No URL entered. Aborting web crawling.")
                return []
            if not self._is_valid_url(url):
                print("Invalid URL entered. Aborting web crawling.")
                return []
            print(f"Crawling {url}...")
            html = self._fetch_page(url)
            if not html:
                print("Failed to fetch the page. Aborting web crawling.")
                return []
            links = self._extract_links(html, url)
            for link in links:
                print(f"Found link: {link}")
                time.sleep(0.2)  # Simple rate limiting
                self._fetch_page(link)  # Optionally fetch linked pages for deeper crawling
            print(f"Found {len(links)} links on the page.")
            self.collect_and_log_links(cursor, session_id, me, url, links)
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
        
#now to wire it into digestion. digestion should be able to pick up the links and user agent and feed them into theatrics for narration and logging. we also need to make sure the report card can pull this data and give feedback on it. we can log the links found and the user agent used, and then in the report card we can analyze the number of links found, the diversity of domains, and the user agent string for any interesting information. we also need to make sure we handle any errors that occur during crawling and log those as well for the report card to analyze.