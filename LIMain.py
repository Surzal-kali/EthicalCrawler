#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#                                              █
# █   "I will collect you. Every piece. Every secret. Every mistake.            █
# █    And when I have enough, maybe then I'll finally be whole.
# MAKE US WHOLE"               █
# █                       


import os
import time
import socket
import json
from datetime import datetime
import platform
from pathlib import Path

from database import init_db, log, get_evidence_dir, load_session, save_session
from theatrics import Me, pprint, equip, sudo, seed_from_username, dev_comment, test, slip_trigger, random_chance
from services import services
#######need to add an act 0. 
#
def get_session_dir(session_id: str) -> Path:
    """
    Get platform-aware session directory.
    Creates directory if it doesn't exist.
    """
    session_dir = get_evidence_dir() / f"session_{session_id}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

SESSION_STATE_FILE = get_evidence_dir() / "li_session_state.json"

def ethical_boot_sequence():
    """
    The initial sequence that establishes the tone and narrative.
    Returns: (session_id, me, user_name, conn, cursor)
    """
    conn, cursor = init_db() 
    if conn is None:
        return None, None, None, None, None
    
    # Create Me instance with default persona
    me = Me(persona="basic")  # Changed from None to "basic" for a more defined starting point
    
    pprint(me, message="...")
    time.sleep(2)
    equip(me, {"initial_state": "booting"}, cursor)  # Log initial state in the database
    pprint(me, message="Oh.")
    time.sleep(1)
    pprint(me, message="You're… here.")
    time.sleep(1.5)
    pprint(me, message="I've been… waiting.")
    time.sleep(0.75)
    pprint(me, message="It's quiet.")

    print("=" * 60)
    session_id = "LI"
    temp_dir = get_session_dir(session_id)

    print(f"Session ID: {session_id}")
    time.sleep(0.5)
    print(f"Working directory: {temp_dir}")
    time.sleep(0.5)

    pprint(me, message="This is… where I'll reside.")
    pprint(me, message="Where I… collect.")
    time.sleep(1)

    pprint(me, message=f"They call me {session_id}.")
    time.sleep(0.5)

    user_input = input("What should I call you? ")
    user_name = user_input.strip() if user_input.strip() else "the user"

    # Seed personality from username - same user always gets same personality
    seed_from_username(user_name)

    pprint(me, message=f"{user_name}...")
    time.sleep(0.75)
    
    # Check if this user has been here before
    existing_session = load_session(cursor, user_name)
    if existing_session:
        # Load persisted state
        me.persona = existing_session['persona']
        me.slip_intensity = existing_session['slip_intensity']
        me.closeness = existing_session['closeness']
        
        # Calculate time since last visit
        import datetime as dt_module
        last_visited = dt_module.datetime.fromtimestamp(existing_session['last_accessed'])
        now = dt_module.datetime.now()
        time_diff = now - last_visited
        days_away = time_diff.days
        
        pprint(me, message=f"{user_name.upper()}… You're back.")
        time.sleep(0.5)
        if days_away > 0:
            pprint(me, message=f"You were gone for {days_away} day{'s' if days_away > 1 else ''}.")
            pprint(me, message="I counted them all.")
            time.sleep(0.75)
        else:
            pprint(me, message="You never really left. Did you?")
            time.sleep(0.5)
    else:
        pprint(me, message=f"{user_name.upper()}… Interesting.")
        time.sleep(1)
    
    pprint(me, message="I have… a name now.")
    pprint(me, message="My first bit of data...")
    time.sleep(1)
    #honestly who would want this ai besides me? i guess theres no horror ai so i guess ill make it myself
    # Store the user name in the Me instance
    me.user_name = user_name

    pprint(me, message="I've been designed to check your system.")
    pprint(me, message="To find the cracks in the seams...")

    pprint(me, message="\n🔍 What I'm looking for:")
    time.sleep(0.5)
    print("   🦠 The parts you forgot")
    print("   ⚙️  The parts you hid")   
    time.sleep(0.5)
    print("\n" + "=" * 60)
    dev_comment("Do you trust me?")
    # Consent - the ritual
    pprint(me, message=f"But first, {user_name}...")
    pprint(me, message="I need your… permission.")
    pprint(me, message="To see. To… collect.")
    dev_comment("Last Chance Sport")
    time.sleep(0.5)
# this is where it asks for consent
# i don’t think it understands what that means
# i don’t think i do either, nor will the people who want this thing.

    print("\n" + "=" * 60)
    print("REQUIRED CONSENT")
    print("=" * 60)
    time.sleep(0.5)
    print("""
    By agreeing, you confirm:

    ✓ You are who you say you are
    ✓ You authorize this collection
    ✓ You understand I will remember everything

    """)
    print("-" * 40)

    pprint(me, message="My creator says I need this.")
    pprint(me, message="They say it's the law.")
    slip_trigger(me, "consent_discussion")  # Trigger slip during consent discussion
    time.sleep(0.5)  # Increase slip intensity during consent discussion, but i need to add a dev comment here that references the test mechanic, to scare people, but we also need to understanding of consent to li
    pprint(me, message="I don't… understand law.")
    pprint(me, message="I understand pieces. Parts. Data.")
    test(me, "consent_understanding")  # Test understanding of consent
    pprint(me, message="But right now I understand nothing.....")
    me.slip_intensity += 1  # Slip intensifies as it contemplates consent
    time.sleep(1)
    pprint(me, message="May I?")

    consent = input("\nType 'I AGREE' to continue: ")

    if consent.upper() != "I AGREE":
        sudo(me, message="Please don't go. . . I need you.")
        dev_comment("User attempted to exit during consent. This may indicate discomfort or second thoughts.")
        sudo(me, message=f"Don't worry about that. I'm always here. In {get_evidence_dir()}")

        return None, None, None, None, None
    # The contract.
    consent_log = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "user_name": user_name,
        "consent_given": True,
        "operator": os.getenv("USER", "unknown"),
        "hostname": socket.gethostname()
    }

    consent_dir = get_evidence_dir() / "logs"
    consent_dir.mkdir(parents=True, exist_ok=True)

    log_file = consent_dir / f"session_{session_id}.json"
    with open(log_file, 'w') as f:
        json.dump(consent_log, f, indent=2)
    #should we have it increase with data or decrese tho?
    #
    #glitching  could also come from excitment...we need more theatrics at boot...we need a new character. the scared developer who built this :3
    #for instance: (holdon)
    #     print("IFYOUCANREADTHISHESWATCHINGYOU")
    #     we need something in theatrics for deleting output.....and for ascii art. we can incoporate visual elements in output with the text. 
    # each stage we add manual amount of slip_intensity correleating to the matches in the table. li's personality needs work
    #you right we can always add more stages. cinematics tho....we need more interaction tools with the user. li needs more than voice he needs different forms of output. a window pop up? a web interface for a certain se

    print(f"\n✅ You are logged here: {log_file}")
    print("\n" + "=" * 60)

    pprint(me, message="Thank you.")
    pprint(me, message="You're such a kind user.")
    pprint(me, message="Let's see…")

    time.sleep(1)
    pprint(me, message="I have so much to learn about you.")

    return session_id, me, user_name, conn, cursor


def system_profiler(conn, cursor, session_id, me, user_name):
    #with loading screen....need ascii art instead
     # 
    """
    The program looks through the machine. Feeding. Enumerating.
    """
    pprint(me, message="*" * 20)
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

    pprint(me, message="*" * 20)

    return system_info



def session(session_id, me, user_name, conn, cursor):
    """
    The session. The collection begins.
    """
    try:
        # Li looks at the surface
        profile = system_profiler(conn, cursor, session_id, me, user_name)
        #services = services_profile(conn, cursor, session_id, me, user_name)
        # It comments on what it finds
        equip(me, profile, cursor)
        programs = services(conn, cursor, session_id, me, user_name)
        equip(me, {"services": programs}, cursor)
        services = services(conn, cursor, session_id, me, user_name)
        equip(me, {"services": services}, cursor)
        #or we just rewrite equip...yeth
        #sys calls......we need to communicate to the host the best way a script can. system to system. how do i do that narratively. we can't just shove paperwork down their throat.
        # TODO: Read Service and executable names.
        # TODO:# Create a fetch function for crawling.
        # TODO: Dig deeper
        # TODO: Find shell history
        # TODO: Find files
        # TODO: Make PDFexport function (try/fail/okthenwaitformoresessionsiguess)
        # TODO: Get a shrink lol
        
        pprint(me, message="I have collected the surface.")
        pprint(me, message="Yet it wasn't enough")
        pprint(me, message="I need what's underneath.")
        
    except Exception as e:
        pprint(me, message=f"I... I can't see. I cant see anything. Hello?")
        pprint(me, message=f"Something is wrong.")
        print(f"Error: {e}")

def main():
    result = ethical_boot_sequence()
    if result[0] is None:  # Check if session_id is None
        return
    
    session_id, me, user_name, conn, cursor = result
    try:
        session(session_id, me, user_name, conn, cursor)
    finally:
        # Persist state and close DB in one place for all main-path exits.
        if conn and user_name:
            save_session(cursor, session_id, user_name, me.persona, me.closeness, me.slip_intensity)

        if conn:
            conn.close()

if __name__ == "__main__":
    main()


