#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is something i guess
import scapy
import requests
from devnotes import notes
###k this time i think i have a realistic idea
import os
import time
import socket
import json
import threading
import subprocess
import sqlite3
import random
import asyncio
from datetime import datetime
from tempfile import TemporaryFile as TF
import platform
import psutil
from database import init_db, log

from theatrics import pprint
from theatrics import pspace

#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is something i guess
import helper
from helper import spawn
import scapy
import requests
from devnotes import notes
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
import psutil
from database import init_db, log
from theatrics import Me, pprint
def analyze_data(process_name):
    if "apache" in process_name.lower():
        quip = Me.quip("apache2")
        pprint(f"Process: {process_name}. Persona says: {quip}")
    elif "ssh" in process_name.lower():
        quip = Me.quip("sshd")
        pprint(f"Process: {process_name}. Persona says: {quip}")
    else:
        pprint(f"logged: {process_name}.")

def ethical_boot_sequence():
    """Core boot sequence with honest consent"""

    pprint("🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱")
    pprint("="*60)

    session_id = f"LI-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/local_inspector_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Session ID: {session_id}")
    print(f"Working directory: {temp_dir}")
    pprint("Alright lets get the housekeeping out of the way. I don't have all day ⌛⌛")
    print("REQUIRED CONSENT:")
    print("="*60)
    print("""
    I confirm that I have:

    ✓ Legal authorization to enumerate this system
    ✓ Local access privileges (either owned or authorized testing)
    ✓ Permission to read configuration files and running processes

    This session will be logged locally for audit purposes.
    """)

    # Make them actually acknowledge
    print("\n" + "-"*40)
    consent = input("Type 'I AGREE' to continue, anything else to exit: ")

    if consent.upper() != "I AGREE":
        pprint("")
        return None

    # Log what they agreed to
    consent_log = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "consent_given": True,
        "acknowledgment": consent,
        "tool_purpose": "post-exploitation enumeration",
        "operator": os.getenv("USER", "unknown"),
        "hostname": socket.gethostname()
    }

    consent_dir = "/tmp/local_inspector_logs/"
    os.makedirs(consent_dir, exist_ok=True)

    log_file = os.path.join(consent_dir, f"session_{session_id}.json")
    with open(log_file, 'w') as f:
        json.dump(consent_log, f, indent=2)

    print(f"\n✅ Consent logged to: {log_file}")
    print("\n" + "="*60)
    pprint("Oh?")
    print("="*60 + "\n")
    return session_id




def system_profiler(cursor, session_id):
    """Enumeration - logs everything to evidence bucket"""

    system_info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor()
    }

    # Log it all
    log(cursor, session_id, "system_profile", system_info)

    # Display as before
    for key, value in system_info.items():
        try:
            analyze_data(value)
        except:
            pprint("uh oh.")
    pprint("This demo may not be optimized for this enviroment\n"
           "I had a pi, windows, and kali, and ubuntu on hand during development\n" \
           "Tread Lightly Traveler")
    return system_info




# def spying(cursor, session_id):
#     """Service enumeration - log findings to evidence bucket"""

#     detected_services = []
#     service_quips = {
#         "apache2": "You know I used to hate apache because i thought it insecure. Apache was my first box 🥹.",
#         "sshd": "Secure Shell detected.  Access granted (maybe). I mean...i won't judge",
#         "mysql": "MySQL is running...thats a nice thread I'd like to explore",
#         "postgresql": "PostgreSQL detected - Hail the mighty elephant lord!",
#         "nginx": "Nginx is amazing. You know it makes for a great web server, but I've never given it a go",
#     }  # Keep your quips

#     services_found = []
#     service_data = []

#     for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
#         proc_name = proc.info['name'].lower()
#         for service, quip in service_quips.items():
#             if service in proc_name:
#                 if service not in services_found:
#                     services_found.append(service)
#                     service_data.append({
#                         'service': service,
#                         'pid': proc.info['pid'],
#                         'memory': proc.info['memory_percent'],
#                         'quip': quip
#                     })
#                     print(f"  {quip}")  # Replace print with print
#                     break

#     # Log everything we found
#     log(cursor, session_id, "services", service_data)

#     # Port scanning results
#     listening_ports = []
#     try:
#         result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, timeout=5)
#         port_output = result.stdout
#     except FileNotFoundError:
#         result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=5)
#         port_output = result.stdout

#     for line in port_output.split('\n'):
#         if 'LISTEN' in line or 'LISTENING' in line:
#             parts = line.split()
#             if len(parts) >= 4:
#                 port_info = parts[3] if 'ss' in str(result.args) else parts[3]
#                 if ':' in port_info:
#                     port = port_info.split(':')[-1]
#                     if port.isdigit() and port not in listening_ports:
#                         listening_ports.append(port)

#     log(cursor, session_id, "open_ports", listening_ports)

#     # Config files found
#     config_paths = {
#         "/etc/ssh/sshd_config": "SSH server config",
#         "/etc/apache2/apache2.conf": "Apache config",
#         # ... etc
#     }

#     configs_found = []
#     for config_path, description in config_paths.items():
#         if os.path.exists(config_path):
#             configs_found.append({'path': config_path, 'description': description})
#             pprint(f"  📄 {description}")  # Replace print with print

#     log(cursor, session_id, "config_files", configs_found)

#     return detected_services

async def main():
    session_id = ethical_boot_sequence()

    if not session_id:
        return

    conn, cursor = init_db(session_id)

    try:
        system_profiler(cursor, session_id)
        analyze_data(session_id)
        conn.commit()
        # generate_pdf_report(conn, session_id)  # Add this later

    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(main())