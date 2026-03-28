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
    #oh hello
    """Core boot sequence - implement THIS first"""
    
    pprint("Initializing EthicalCrawler...")

    #wakeywakey everybody sound off
    
    session_id = f"EC-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/ethicalcrawler_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)

    pprint(f"Session ID: {session_id}")
    pprint(f"Temp directory: {temp_dir}")

###am i allowed to invite friends?
    consent_dir = "/consent/"
    if not os.path.exists(consent_dir):
        os.makedirs(consent_dir, exist_ok=True)
        pprint(f"Created consent directory: {consent_dir}")
        time.sleep(5)
    # 3. Display consent screen
    pprint("\n" + "="*60)
    pprint("ETHICAL OPERATOR CONSENT REQUIRED")
    pprint("="*60)
    pprint("\nI acknowledge that this session will be logged for transparency.")
    pprint("All actions will target only systems I own or have permission to test.")
    
    consent = input("\nType 'n' to quit, anything else to continue: ")
    
    if consent == "n":
        pprint("Consent not provided. Exiting.")
        return consent
    
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
    
    pprint(f"\nConsent logged to: {log_file}")
    pprint("\n" + "="*60 +"\n")
    pprint("BOOT SEQUENCE COMPLETE")
    pprint("="*60 + "\n")

def system_profiler():
    ####enumeration time bb
    system_info = {}
    system_info['os_name'] = platform.system()
    system_info['os_version'] = platform.version()
    system_info['architecture'] = platform.machine()
    system_info['processor'] = platform.processor()

    for key, value in system_info.items():
        pprint(f"  {key}: {value}\n")

    pprint(f"This program may not be optimized for the following specs. Proceed with caution.\n")
    pprint(f"All modules are considered optional, and will not be attempted without explicit consent.\n")
    pprint(f"*"*60)
    pprint(f"DEV NOTES:  \n")
    pprint(f"this is my god's honest attempt at making:\n")
    pprint("1. A legal and ethical black-box automated pen test.\n")
    pprint("2. An overly ambitious Python Basics final\n")        
    pprint("Enjoy the show") ### also im gunna try to make these comments gold k? 
    pprint(f"="*60 + "\n")
    return system_info

def spying():
    """Take roll call on running services - read-only, no active probing"""
    
    pprint("It's time to see what you've got tho\n")
    pprint("Enough about me tell me about you?")
    pprint("="*60)
    
    detected_services = []
    
    # Personality quips dictionary for common services
    service_quips = {
        "ssh": "🔑 You have guests on your ssh tunnel. Were they invited?",
        "sshd": "🔑 OOO sshd is listening on socket? Can i have your number? Can I?",
        "apache": "🌐 Oh my my my apache huh? Gotta love apache.",
        "httpd": "🌐 Web server detected. Can i get the addy?",
        "mysql": "🗄️ MySQL database running. Sounds like a thread to pull to me!",
        "postgres": "🐘 PostgreSQL spotted. Make way for the almighty elephant god!!!",
        "docker": "🐳 Docker containers sailing. Whats sailing through doc?",
        "redis": "🔴 Redis is caching. In-memory shennanigans indeed!!",
        "mongodb": "🍃 MongoDB running. Hopefully not documenting me (❁´◡`❁)",
        "cron": "⏰ Cron daemon awake. Sounds like you have some services you're awfully dependant on.",
        "systemd": "⚙️ systemd is watching. Always watching. But who watches the watcher?",
        "fail2ban": "🛡️ Fail2ban on duty. Papi no its me",
        "ufw": "🔥 UFW firewall active. Thats....interesting......",
        "iptables": "📜 oh i hope you let me",
        "snmpd": "📡 SNMP running. Hope the community strings are secret!",
    }

    # Check running processes for common services
    pprint("🔍 RUNNING SERVICES:")
    pprint("-" * 40)
    
    services_found = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        proc_name = proc.info['name'].lower()
        # Check if this process matches any known service
        for service, quip in service_quips.items():
            if service in proc_name:
                if service not in services_found:
                    services_found.append(service)
                    pprint(f"  {quip}")
                    detected_services.append(proc.info['name'])
                    break
    
    if not services_found:
        pprint("  🤔 No common services detected. You're no fun")
    
    # Get listening ports (read-only, no connections)
    pprint("\n🔌 OPEN PORTALS (LISTENING):")
    pprint("-" * 40)
    
    # Try ss first (modern), fall back to netstat
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True, timeout=5)
        port_output = result.stdout
    except FileNotFoundError:
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, timeout=5)
        port_output = result.stdout
    
    # Parse and display ports with some personality
    listening_ports = []
    for line in port_output.split('\n'):
        if 'LISTEN' in line or 'LISTENING' in line:
            # Extract port number (simplified)
            parts = line.split()
            if len(parts) >= 4:
                port_info = parts[3] if 'ss' in str(result.args) else parts[3]
                if ':' in port_info:
                    port = port_info.split(':')[-1]
                    if port.isdigit() and port not in listening_ports:
                        listening_ports.append(port)
                        # Fun port commentary
                        port_comments = {
                            "22": "   🚪 Port 22: SSH - The digital front door",
                            "80": "   🌐 Port 80: HTTP - Unencrypted web traffic",
                            "443": "   🔒 Port 443: HTTPS - Secure web traffic",
                            "3306": "   🗄️ Port 3306: MySQL - Database listening",
                            "5432": "   🐘 Port 5432: PostgreSQL - Elephant ears open",
                            "27017": "   🍃 Port 27017: MongoDB - Document store",
                            "6379": "   🔴 Port 6379: Redis - Cache ready",
                            "8080": "   🎨 Port 8080: Alternative web - Hipster port",
                            "25": "   📧 Port 25: SMTP - Sending mail vibes",
                            "53": "   🌐 Port 53: DNS - Who's translating?",
                        }
                        if port in port_comments:
                            pprint(port_comments[port])
                        else:
                            pprint(f"   🔌 Port {port}: Something's listening here...")
    
    if not listening_ports:
        pprint("  🕵️ No listening ports found. Stealth mode activated!")
    
    # Check for common config files (read-only existence check)
    pprint("\n📁 CONFIGURATION SIGNATURES:")
    pprint("-" * 40)
    
    config_paths = {
        "/etc/ssh/sshd_config": "SSH server config present",
        "/etc/apache2/apache2.conf": "Apache config found",
        "/etc/nginx/nginx.conf": "Nginx configuration",
        "/etc/mysql/my.cnf": "MySQL configuration",
        "/etc/docker/daemon.json": "Docker daemon config",
        "/etc/fail2ban/jail.conf": "Fail2ban jail config",
        "/etc/ufw/ufw.conf": "UFW firewall config",
    }
    
    for config_path, description in config_paths.items():
        if os.path.exists(config_path):
            pprint(f"  📄 {description}")
            # Don't read the file, just acknowledge existence
    
    # System load overview (safe read)
    pprint("\n📊 SYSTEM VITALS:")
    pprint("-" * 40)
    try:
        load_avg = os.getloadavg()
        pprint(f"  📈 Load Average: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
    except AttributeError:
        # Windows doesn't have loadavg
        pass
    
    # Who's logged in (safe read)
    try:
        result = subprocess.run(['who'], capture_output=True, text=True, timeout=5)
        if result.stdout.strip():
            user_count = len(result.stdout.strip().split('\n'))
            pprint(f"  👥 Logged in users: {user_count}")
    except subprocess.TimeoutExpired:
        pprint("  ⏱️ Service enumeration timed out (system may be busy)")
    except FileNotFoundError:
        pprint("  ⚠️ 'who' command not found")
    
    pprint("\n" + "="*60)
    pprint(f"📝 Attack Surface Expanded! {len(detected_services)} services identified.")
    
    return detected_services
async def main():
    system_profiler()
    consent = ethical_boot_sequence()
    if consent != "n":
        notes()
        spying()
    else:
        pass


if __name__ == "__main__":
    asyncio.run(main())



