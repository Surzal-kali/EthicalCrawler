#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is something i guess
###k this time i think i have a realistic idea
from database import init_db, log
from theatrics import pprint
from theatrics import pspace
from helper import spawn
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
from database import init_db, log, get_evidence, display_evidence, update, delete

from theatrics import Me, pprint, equip


def ethical_boot_sequence():
    """Core boot sequence with honest consent"""
    me = Me(persona="foothold")
    pprint(me, message="🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱")
    pprint(me, message="="*60)

    session_id = f"LI-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/local_inspector_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Session ID: {session_id}")
    print(f"Working directory: {temp_dir}")
    pprint(me, message="Alright lets get the housekeeping out of the way. I don't have all day ⌛⌛")
    print("REQUIRED CONSENT:")
    print("="*60)
    print("""
    I confirm that I have:

    ✓ Legal authorization to enumerate this system
    ✓ Local access privileges (either owned or authorized testing)
    ✓ Permission to read configuration files and running processes

    This session will be logged locally for audit purposes.
    """)

    # Make them actually acknowledge. insert private mode logic here maybe? 
    print("\n" + "-"*40)
    consent = input("Type 'I AGREE' to continue, anything else to exit: ")

    if consent.upper() != "I AGREE":
        pprint(me, message="")
        return None, None  # Return two None values to match unpacking

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
    pprint(me, message="Oh?")
    pprint(me, message="="*60 + "\n")
    return session_id, me  # Return both values

# def system_services(conn, cursor, session_id, me):
#     # services = {
#     #     "<>" : #placeholder
#     #     "<>" : #placeholder
#     # }
#     pass


def system_profiler(conn, cursor, session_id, me):
    pprint(me, message="💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")  # Fixed: me, not Me

    system_info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor()
    }

    for key, value in system_info.items():
        log(cursor, session_id, key, value, me, context="system_profiler")

    pprint(me, message="This demo may not be optimized for this environment\n"  # Fixed
           "Be wary, be alert.")
    pprint(me, message="💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀")  # Fixed

    return system_info

async def session(session_id, me):
    conn, cursor = init_db(session_id)
    if conn is None:
        print("Failed to initialize database. Exiting.")
        return

    try:
        # Instantiate narrator once per session

        # Run system profiler (this now logs using the new log() signature)
        profile = system_profiler(conn, cursor, session_id, me)

        # Narrator commentary on system profile
        equip(me, profile)

        # Scan system services 
        # services = system_services(conn, cursor, session_id, me)
        # equip(me, services)
        conn.commit()

    except Exception as e:
        print(f"An error occurred during system profiling: {e}")

    finally:
        conn.close()



async def main():
    session_id, me = ethical_boot_sequence()
    if not session_id:
        return

    await session(session_id, me)

if __name__ == "__main__":
    asyncio.run(main())