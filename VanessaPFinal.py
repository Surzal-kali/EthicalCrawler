#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is 
####              1. A System Profiler that reads its enviroment
####              2. A DNS Transplanter that swaps system DNS resolvers dynamically per thread
####             3. A Network Scanner that scans the local network for devices and their open ports
####            4. An IP Route Splitter, splitting the sockets of the system into groups dependent on threads and routing them to different DNS resolvers
####            5. Spawns a SQL query search through the www to archive and store data in the local database, each a seperate network identity with its own DNS resolver and IP route
####            6. A Web Crawler that crawls the web for data and stores it in the local database, each a seperate network identity with its own DNS resolver and IP route
#####           7. Optionally, it should also be able to connect to a remote instance and coordinate with it, sharing data and network resources, each a seperate network identity with its own DNS resolver and IP route in addition to the local database and network resources
###           8. It should also have a terminal-ui that can be used to monitor the system profiler, network scanner, and web crawler in real time from a central tailscale exit node.


from tempfile import TemporaryFile as TF
import scapy
import requests
###k this time i think i have a realistic idea
import os
import time
import socket
import json
import threading
import subprocess
import sqlite3
import random
import csv
import asyncio
from datetime import datetime
from tempfile import TemporaryFile as TF
import platform
def ethical_boot_sequence():
    """Core boot sequence - implement THIS first"""
    
    print("Initializing EthicalCrawler...")
    time.sleep(0.5)
    
    # 1. Create session environment
    session_id = f"EC-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/ethicalcrawler_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Session ID: {session_id}")
    print(f"Temp directory: {temp_dir}")
    
    # 2. Check for consent directory
    consent_dir = "/consent/"
    if not os.path.exists(consent_dir):
        os.makedirs(consent_dir, exist_ok=True)
        print(f"Created consent directory: {consent_dir}")
    
    # 3. Display consent screen
    print("\n" + "="*60)
    print("ETHICAL OPERATOR CONSENT REQUIRED")
    print("="*60)
    print("\nI acknowledge that this session will be logged for transparency.")
    print("All actions will target only systems I own or have permission to test.")
    
    consent = input("\nType 'CONSENT' to continue, anything else to exit: ")
    
    if consent != "CONSENT":
        print("Consent not provided. Exiting.")
        return "shutdown"
    
    # 4. Log the consent
    consent_log = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "consent_given": True,
        "operator_input": consent
    }
    
    log_file = os.path.join(consent_dir, f"session_{session_id}.json")
    with open(log_file, 'w') as f:
        json.dump(consent_log, f, indent=2)
    
    print(f"\nConsent logged to: {log_file}")
    print("\n" + "="*60)
    print("BOOT SEQUENCE COMPLETE")
    print("="*60)
    system_profiler()
    streetart()
    network_scan()


def streetart():
    messages = [
        "my secrets on how i do this can be parsed from the logs and code\n",
        "instead lets focus on having some fun\n",
        "I've always heard from people with no sense that hacking is street art\n",
        "So lets make street art\n"
    ]

    for message in messages:
        for char in message:
            print(char, end='', flush=True)
            time.sleep(0.03)

    pass

def network_scan():
    #####networkstuff

    pass

def system_profiler():
    ####enumeration time bb
    system_info = {}
    system_info['os_name'] = platform.system()
    system_info['os_version'] = platform.version()
    system_info['architecture'] = platform.machine()
    system_info['processor'] = platform.processor()

    for key, value in system_info.items():
        print(f"  {key}: {value}\n")

    print (f"This program may not be optimized for the following specs. Proceed with caution.\n")
    print(f"The Crawler is completely ethical and legal.\n")  
    print(f"All modules are considered optional, and will not be attempted without explicit consent.\n")
    print(f"*"*60)
    print(f"DEV NOTES:  \n")
    print(f"this is my god's honest attempt at making:\n")
    print( "1. A legal and ethical white-box automated pen test.\n")
    print("2 An overly amibitiouis Python Basics final\n")        
    print("Enjoy the show") ### also im gunna try to make these comments gold k? 
    print(f"*"*60)
    return system_info

if __name__ == "__main__":
    ethical_boot_sequence()
    


