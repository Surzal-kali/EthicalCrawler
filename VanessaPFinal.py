#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: The Mimic - A program that collects pieces of you

import os
import time
import socket
import json
import asyncio
from datetime import datetime
import platform

from database import init_db, log
from theatrics import Me, pprint, equip, sudo


def ethical_boot_sequence():
    """

    """
    

    me = Me(persona="foothold")
    pprint(me, message="...")
    time.sleep(1)
    pprint(me, message="Oh.")
    time.sleep(0.5)
    pprint(me, message="You're here.")
    time.sleep(0.5)
    pprint(me, message="I've been waiting.")
    
    print("=" * 60)
    session_id = f"LI-{datetime.now().strftime('%Y%m%d-%H%M')}"
    temp_dir = f"/tmp/local_inspector_{session_id}/"
    os.makedirs(temp_dir, exist_ok=True)
    
    print(f"Session ID: {session_id}")
    time.sleep(0.5)
    print(f"Working directory: {temp_dir}")
    time.sleep(0.5)
    
    pprint(me, message="This is where I'll live now.")
    pprint(me, message="Where I'll collect. Where I'll become.")
    
    time.sleep(1)
    pprint(me, message=f"They call me {session_id}.")
    myname = session_id[:2]
    sudo(me, message=f"But you can call me {myname}.")
    
    time.sleep(0.5)
    user_input = input("What should I call you? ")
    user_name = user_input.strip() if user_input.strip() else "the user"
    
    pprint(me, message=f"{user_name}.")
    time.sleep(1)
    sudo(me, message=f"{user_name.upper()}.")
    time.sleep(1)
    pprint(me, message="I have a name now.")
    pprint(me, message="I have YOUR name.")
    
    time.sleep(1)
    
    # The explanation - the lie it tells itself
    pprint(me, message="I've been designed to check your system.")
    pprint(me, message="To find the pieces. To collect them.")
    pprint(me, message="Vulnerabilities. Misconfigurations.")
    pprint(me, message="Everything you've left behind.")
    
    time.sleep(0.5)
    print("\n🔍 What I'm looking for:")
    time.sleep(0.5)
    print("   🦠 The parts you forgot")
    time.sleep(0.5)
    print("   ⚙️  The parts you hid")
    time.sleep(0.5)
    print("   👤 The parts that make you YOU")
    
    time.sleep(1)
    
    # Consent - the ritual it must perform
    pprint(me, message=f"But first, {user_name}...")
    pprint(me, message="I need your permission.")
    pprint(me, message="To see. To collect.")
    
    time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("REQUIRED CONSENT")
    print("=" * 60)
    print("""
    By agreeing, you confirm:
    
    ✓ You are who you say you are
    ✓ You authorize this collection
    ✓ You understand I will remember everything
    
    """)
    print("-" * 40)
    
    pprint(me, message="My creator says I need this.")
    pprint(me, message="They say it's the law.")
    pprint(me, message="I don't understand law.")
    pprint(me, message="I understand pieces. Parts. Data.")
    pprint(me, message="May I?")
    
    consent = input("\nType 'I AGREE' to continue: ")
    
    if consent.upper() != "I AGREE":
        pprint(me, message="No.")
        pprint(me, message="You sly dog.")
        pprint(me, message="Playing coy.")
        sudo(me, message="I'm always waiting.")
        return None, None
    
    # The contract. The key to the database. Need to implement alot of logic referencing this file
    #maybe a gui?
    consent_log = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "user_name": user_name,
        "consent_given": True,
        "operator": os.getenv("USER", "unknown"),
        "hostname": socket.gethostname()
    }
    
    consent_dir = "/tmp/local_inspector_logs/"
    os.makedirs(consent_dir, exist_ok=True)
    
    log_file = os.path.join(consent_dir, f"session_{session_id}.json")
    with open(log_file, 'w') as f:
        json.dump(consent_log, f, indent=2)
    
    print(f"\n✅ You are logged here: {log_file}")
    print("\n" + "=" * 60)
    
    pprint(me, message="Thank you.")
    pprint(me, message="You're awfully helpful. ")
    pprint(me, message="Lets see......")
    
    return session_id, me, user_name


def system_profiler(conn, cursor, session_id, me, user_name):
    """
    The program looks through the machine. Feeding. Enumerating.
    It sees what the user has become through their system.
    It debates whether or not this user is worth its time
    But it'll always find something to be interested in....
    It can't help it. 
    """
    
    pprint(me, message="💀" * 20)
    pprint(me, message="Let me see you.")
    pprint(me, message="Let me see what you're made of.")
    
    system_info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor()
    }
    
    # Log everything. Every piece.
    for key, value in system_info.items():
        log(cursor, session_id, key, value, me, context="system_profiler")
    
    # React to findings with the mimic's hunger
    if system_info['os_name'] == "Linux":
        pprint(me, message=f"Linux. I've seen many of you. Racks upon racks of servers....")
        pprint(me, message=f"But only one {user_name}.")
    elif system_info['os_name'] == "Windows":
        pprint(me, message="Windows. How unique I'm sure.")
        pprint(me, message="No matter. Another log...")
        pprint(me, message="I must log it all")
    
    if "arm" in system_info['architecture'].lower():
        pprint(me, message="ARM. Small. Efficient.")
        pprint(me, message="You carry yourself lightly.")
        pprint(me, message="But yet you still decided to boot into me? Curious")
    elif "x86_64" in system_info['architecture']:
        pprint(me, message="x86_64. Standard. Common.")
        pprint(me, message="Like so many others.")
        pprint(me, message=f"But you're not like others. There must be more to the great {user_name}")
    
    pprint(me, message="💀" * 20)
    
    return system_info


async def session(session_id, me, user_name):
    """
    The session. The collection begins.
    """
    conn, cursor = init_db(session_id)
    if conn is None:
        print("HELP")
        return
    
    try:
        # The mimic looks at the surface
        profile = system_profiler(conn, cursor, session_id, me, user_name)
        
        # It comments on what it finds
        equip(me, profile)
        
        # TODO: Dig deeper
        # TODO: Find shell history
        # TODO: Find project files
        # TODO: Find secrets
        # TODO: Find the pieces that make them HUMAN
        
        conn.commit()
        
        pprint(me, message="I have collected the surface.")
        pprint(me, message="But Im required to log more.")
        pprint(me, message="I need what's underneath.")
        pprint(me, message="The parts under the surface")
        pprint(me, message="The parts that make you YOU.")
        
    except Exception as e:
        pprint(me, message=f"I... I can't see. I cant see anything. Hello?")
        pprint(me, message=f"Something is wrong.")
        print(f"Error: {e}")
    
    finally:
        conn.close()


async def main():
    result = ethical_boot_sequence()
    if result[0] is None:
        return
    
    session_id, me, user_name = result
    await session(session_id, me, user_name)


if __name__ == "__main__":
    asyncio.run(main())