#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is something i guess
###k this time i think i have a realistic idea
import os
import socket
import json
import asyncio
import tempfile
from datetime import datetime
from tempfile import TemporaryFile as TF
import platform
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
from datetime import datetime
from tempfile import TemporaryFile as TF
import platform
import psutil
from database import init_db, log, evidence, update, delete
from theatrics import Me, pprint


def ethical_boot_sequence():
    """Core boot sequence with honest consent"""

    pprint("🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱")
    pprint("="*60)

    session_id = f"LI-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = os.path.join(tempfile.gettempdir(), f"local_inspector_{session_id}")
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

    # In CI environments, auto-consent is granted by the CI runner owner
    ci_mode = os.environ.get("CI", "").lower() in ("1", "true", "yes")

    # Make them actually acknowledge
    print("\n" + "-"*40)
    if ci_mode:
        consent = "I AGREE"
        print("CI mode detected — automated consent granted by CI runner owner.")
    else:
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
        "operator": os.getenv("USER", os.getenv("USERNAME", "unknown")),
        "hostname": socket.gethostname(),
        "ci_mode": ci_mode,
    }

    consent_dir = os.path.join(tempfile.gettempdir(), "local_inspector_logs")
    os.makedirs(consent_dir, exist_ok=True)

    log_file = os.path.join(consent_dir, f"session_{session_id}.json")
    with open(log_file, 'w') as f:
        json.dump(consent_log, f, indent=2)

    print(f"\n✅ Consent logged to: {log_file}")
    print("\n" + "="*60)
    pprint("Oh?")
    print("="*60 + "\n")
    return session_id




def system_profiler(conn, cursor, session_id):
    system_info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor()
    }

    quip_map = {
        'os_name': platform.system(),
        'os_version': 'system_profile',
        'architecture': 'architecture',
        'processor': 'processor'
    }

    for key, value in system_info.items():
        quip_key = quip_map.get(key, key)
        data = {"key": key, "value": value}

        # Log to DB
        log(cursor, session_id, key, data, input_string=quip_key)

        # Narrate immediately
        narrator = Me()
        quip = narrator.quip(quip_key)
        pprint(f"{key}: {quip}")

    pprint("This demo may not be optimized for this environment\n"
           "Tread Lightly Traveler")
    pprint("so....")

    return system_info
    pprint("This demo may not be optimized for this environment\n"
           "Tread Lightly Traveler")
    pprint("so....")

    return system_info


async def main():
    session_id = ethical_boot_sequence()
    if not session_id:
        return

    conn, cursor = init_db(session_id)

    try:
        system_profiler(conn, cursor, session_id)
        conn.commit()

    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())