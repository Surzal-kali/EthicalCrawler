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

def pspace(message, char_delay=0.03, line_delay=0.5):
        print("\n")
        for char in message:
            print(char, end='', flush=True)
            time.sleep(char_delay)
            time.sleep(line_delay)
        print("\n")
def pprint(message, char_delay=0.03, line_delay=0.5):
    print ("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print ("\n")

def ethical_boot_sequence(): 
    """Core boot sequence with honest consent"""
    
    pprint("🔍 Local Inspector v0.1 - Post-Exploitation Enumeration Suite")
    pprint("="*60)
    
    session_id = f"LI-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/local_inspector_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)
    
    pprint(f"Session ID: {session_id}")
    pprint(f"Working directory: {temp_dir}")
    
    # Display what this tool ACTUALLY does
    pprint("\n" + "="*60)
    pprint("WHAT THIS TOOL DOES:")
    pprint("="*60)
    pprint("""    
    This tool enumerates a compromised system to discover:
    
    • Running services and open ports
    • Installed applications and their configurations  
    • Privilege escalation paths (SUID binaries, cron jobs, sudo)
    • Credential locations (SSH keys, config files, history)
    • Network layouts and pivot opportunities
    • Sensitive data locations
    
    It assumes you already have local access to this system.
    """)
    
    pprint("="*60)
    pprint("REQUIRED CONSENT:")
    pprint("="*60)
    pprint("""
    I confirm that I have:
    
    ✓ Legal authorization to enumerate this system
    ✓ Local access privileges (either owned or authorized testing)
    ✓ Permission to read configuration files and running processes
    
    This session will be logged locally for audit purposes.
    """)
    
    # Make them actually acknowledge
    pprint("\n" + "-"*40)
    consent = input("Type 'I AGREE' to continue, anything else to exit: ")
    
    if consent.upper() != "I AGREE":
        pprint("\n❌ Consent not provided. Exiting.")
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
    
    pprint(f"\n✅ Consent logged to: {log_file}")
    pprint("\n" + "="*60)
    pprint("🚀 Beginning local enumeration...")
    pprint("="*60 + "\n")










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
        pprint(f"  {key}: {value}\n")
    
    return system_info

def spying():
    """Service enumeration - log findings to evidence bucket"""
    
    detected_services = []
    service_quips = { ... }  # Keep your quips
    
    services_found = []
    service_data = []
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        proc_name = proc.info['name'].lower()
        for service, quip in service_quips.items():
            if service in proc_name:
                if service not in services_found:
                    services_found.append(service)
                    service_data.append({
                        'service': service,
                        'pid': proc.info['pid'],
                        'memory': proc.info['memory_percent'],
                        'quip': quip
                    })
                    pprint(f"  {quip}")
                    break
    
    # Log everything we found
    log(cursor, session_id, "services", service_data)
    
    # Port scanning results
    listening_ports = []
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, timeout=5)
        port_output = result.stdout
    except FileNotFoundError:
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=5)
        port_output = result.stdout
    
    for line in port_output.split('\n'):
        if 'LISTEN' in line or 'LISTENING' in line:
            parts = line.split()
            if len(parts) >= 4:
                port_info = parts[3] if 'ss' in str(result.args) else parts[3]
                if ':' in port_info:
                    port = port_info.split(':')[-1]
                    if port.isdigit() and port not in listening_ports:
                        listening_ports.append(port)
    
    log_evidence(cursor, session_id, "open_ports", listening_ports)
    
    # Config files found
    config_paths = {
        "/etc/ssh/sshd_config": "SSH server config",
        "/etc/apache2/apache2.conf": "Apache config",
        # ... etc
    }
    
    configs_found = []
    for config_path, description in config_paths.items():
        if os.path.exists(config_path):
            configs_found.append({'path': config_path, 'description': description})
            pprint(f"  📄 {description}")
    
    log_evidence(cursor, session_id, "config_files", configs_found)
    
    return detected_services
async def main():
    session_id = ethical_boot_sequence()
    
    if not session_id:
        return
    
    conn, cursor = init_db(session_id)
    
    try:
        system_profiler(cursor, session_id)
        spying(cursor, session_id)  

        conn.commit()
        # generate_pdf_report(conn, session_id)  # Add this later
        
    finally:
        conn.close()