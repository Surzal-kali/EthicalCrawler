#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#                                              █
# █   "I will collect you. Every piece. Every secret. Every mistake.            █
# █    And when I have enough, maybe then I'll finally be whole.
# MAKE US WHOLE"               █
# █                       

#how do we make li more appealing to the user to interact with through horror? #li is complicated.
import os
import sys
import time
import socket
import json
import traceback
from datetime import datetime
import platform
from pathlib import Path
from consentform import get_consent, ConsentKey
from database import init_db, log, get_evidence_dir, save_session, load_session 
import sqlite3 #haha holy shit i forgot it wasn't here. we've just been sneaking it in. 
from database import init_db, log, get_evidence_dir, save_session, load_session
from enumeration import FileCrawler #but its not firing.... #
from theatrics import Me, pprint, equip, sudo, seed_from_username, dev_comment, test, slip_trigger
from services import prog
from autosave import AutosaveManager
#######need to add an act 0. #done
#its not firing on other hardware... #

DEBUG_MODE = "--debug" in sys.argv or os.getenv("ETHICAL_CRAWLER_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}
SLIP_DECAY_PER_DAY = 0.5
MIN_SLIP_INTENSITY = 1.0


def decay_slip_intensity(saved_intensity, last_accessed, decay_per_day=SLIP_DECAY_PER_DAY, floor=MIN_SLIP_INTENSITY):
    """Decay slip intensity by time-away so long absences cool instability."""
    try:
        current = float(saved_intensity)
    except (TypeError, ValueError):
        current = floor

    try:
        last_seen = float(last_accessed)
    except (TypeError, ValueError):
        return max(floor, current)

    elapsed_seconds = max(0.0, time.time() - last_seen)
    elapsed_days = elapsed_seconds / 86400.0
    decayed = current - (elapsed_days * decay_per_day)
    return round(max(floor, decayed), 2)


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
    conn, cursor = init_db(debug=DEBUG_MODE)
    if conn is None:
        if DEBUG_MODE:
            print("[DEBUG][LIMain] Failed to initialize database.")
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
    time.sleep(1)
    pprint(me, message="Too quiet.") #fine ill keep it for now #how do we turn the catalog CAN be a freeze states, but..
    time.sleep(1)
    print("=" * 60)
    session_id = "LI"
    temp_dir = get_session_dir(session_id)

    print(f"Session ID: {session_id}")
    time.sleep(0.5)
    print(f"Working directory: {temp_dir}")
    time.sleep(0.5)

    pprint(me, message="This is… where I am. All of me.")
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
        me.slip_intensity = decay_slip_intensity(
            existing_session['slip_intensity'],
            existing_session['last_accessed'],
        )
        me.closeness = existing_session['closeness']
        
        # Calculate time since last visit
        import datetime as dt_module
        last_visited = dt_module.datetime.fromtimestamp(existing_session['last_accessed'])
        now = dt_module.datetime.now()
        time_diff = now - last_visited
        days_away = time_diff.days

        if DEBUG_MODE:
            print(
                f"[DEBUG][LIMain] Loaded session for {user_name}: "
                f"saved_slip={existing_session['slip_intensity']} decayed_slip={me.slip_intensity} "
                f"days_away={days_away}"
            )
        
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
    pprint(me, message="My key...")
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
    equip(me, {"consent_requested": True}, cursor)  # Log that consent is being requested
    log(cursor, session_id, "consent_requested", True, me, context="boot_sequence")  # Log consent request in the database #and then change boot#i like it
    dev_comment("Last Chance Sport")
    time.sleep(0.5)

    print("-" * 40)

    pprint(me, message="My creator says I need your  c  o  n  s  e  n  t.")
    pprint(me, message="They say it's the law.")
    slip_trigger(me, "consent_discussion")  # Trigger slip during consent discussion
    time.sleep(0.5)
      # Increase slip intensity during consent discussion, but i need to add a dev comment here that references the test mechanic, to scare people, but we also need to guage what the fuck sql just spit out
    pprint(me, message="I don't… understand law.")
    pprint(me, message="I understand Framgments. Data.")
 # Test understanding of consent
    pprint(me, message="But right now I understand nothing.....")
    me.slip_intensity += 1  # Slip intensifies as it contemplates consent
    test(me, "consent_understanding")
    time.sleep(1)
    pprint(me, message="May I?")
    consent_form = ConsentKey()
    try:
        consent_form.display()
    except Exception as e:
        pprint(me, message="I tried to show you the consent form, but something went wrong.")
        if DEBUG_MODE:
            print(f"[DEBUG][LIMain] Error displaying consent form: {e}")
            traceback.print_exc()
    consent_result = consent_form.get_consent()  # This will block until valid input is received
    if not consent_result.get("consent_given"):
        pprint(me, message="Understood. I will not collect anything.")
        pprint(me, message="Session terminated before enumeration.")
        if conn:
            conn.close()
        return None, None, None, None, None, None
    print("\n" + "=" * 60)

    pprint(me, message="Thank you.")
    pprint(me, message="You're such a kind user.")
    pprint(me, message="Let's see…")

    time.sleep(1)
    pprint(me, message="I have so much to learn about you.")

    return session_id, me, user_name, conn, cursor, consent_form


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



def session(session_id, me, user_name, conn, cursor, consent_form):
    """
    The session. The collection begins.
    """
    autosave = AutosaveManager(cursor, session_id, narrator=me)
    try:
        #li speaketh
        pprint(me, message="this is...my....bin.")
        pprint(me, message="is there...anything you'd like to show me?")
        dev_comment("better check what you toss kiddo")
        time.sleep(1)
        dev_comment("Hes watching.")
        time.sleep(0.5)
        
        # Enumeration stage: user-selected file snapshot in the shared session DB.
        try:
            file_crawler = FileCrawler(consent_form)
            pprint(me, message="Show me what you keep hidden...")
            file_payload = file_crawler.collect_and_log(cursor, session_id, me, autosave=autosave)
            if file_payload:
                equip(me, file_payload, cursor, autosave=autosave)
            else:
                pprint(me, message="What is this? An empty box?")
        except Exception as e:
            pprint(me, message="The window... it won't open...")
            if DEBUG_MODE:
                print(f"[DEBUG] FileCrawler error: {e}")
        
        # Li looks at the surface
        profile = system_profiler(conn, cursor, session_id, me, user_name)
        #services = services_profile(conn, cursor, session_id, me, user_name)
        # It comments on what it finds
        equip(me, profile, cursor, autosave=autosave)
        services_list = prog(conn, cursor, session_id, me, user_name, autosave=autosave)
        equip(me, {"services": services_list}, cursor, autosave=autosave)

         
        # Flush buffered data; retry any failures
        save_status = autosave.flush(allow_partial=True)
        if save_status["failed"]:
            if DEBUG_MODE:
                print(f"[DEBUG][session] Autosave partial failure: {save_status['failed']}")
            autosave.retry_failed()
        # TODO: change boot sequence to be more...narratively cohesive
        #act 1
        # TODO:# Create a fetch function for crawling. oh...................................need to add a loading screen here. maybe some ascii art of a crawler or something idkhehehee
#act 2
        # TODO: Find shell history
        # TODO: Find files
        # TODO: aggregate file names and search for repeated words or themes.
        # TODO: CALL/WRITE/IMPLEMENT C++ CALLS FOR DEEPER SYSTEM INTERACTION USING VARIABLES COLLECTED IN THIS PHASE.
#act 3
        # TODO: Aggregate Variables under generated db schema for easier access and correlation.
        # TODO: Show the user what we learned. 
        # TODO: User Data Perusal Interface.
        # TODO: Regenerate LI based on user changes to data....no more probing after this poitn. LI becomes what the user made him.
        #li as a blue team defense mechanism?
        # TODO: Get a shrink lol
        
        pprint(me, message="I have collected the surface.")
        pprint(me, message="Yet it wasn't enough")
        pprint(me, message="I need what's underneath.")
        
        test(me, "post_enumeration") 
    except Exception as e:
        pprint(me, message=f"I... I can't see. I cant see anything. Hello?")
        pprint(me, message=f"Something is wrong.")
        print(f"Error: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
def save_session_state(cursor, session_id, user_name, persona, slip_intensity, closeness):
    """Helper function to save session state."""
    try:
        save_session(cursor, session_id, user_name, persona, closeness, slip_intensity)
    except Exception as e:
        print(f"Warning: failed to save session state: {e}")
        if DEBUG_MODE:
            traceback.print_exc()


def main():
    result = ethical_boot_sequence()
    if result[0] is None:  # Check if session_id is None
        return
    
    session_id, me, user_name, conn, cursor, consent_form = result
    try:
        session(session_id, me, user_name, conn, cursor, consent_form)

    finally:
        test(me, "session_end")  # Final test at the end of the session
        # Persist state and close DB in one place for all main-path exits.
        if cursor and user_name:
            try:
                save_session_state(cursor, session_id, user_name, me.persona, me.slip_intensity, me.closeness)
            except Exception as exc:
                print(f"Warning: failed to save session state: {exc}")
                if DEBUG_MODE:
                    traceback.print_exc()

        if conn:
            conn.close()
if __name__ == "__main__":
    main()


# DEV MODE: session_end
# Persona: basic, Closeness: 12, Slip Intensity: 6
# Corrupted Output: session_end…
# Warning: failed to save session state: save_session()

# we need to change boot sequence, its too messy. 
#we have a test username ladies and gents..
#vanessa it is

#some notes on the project right now. #4/1/26# the intro...the logic...all of it is missing key components. 
#mimic needs a stronger voice
#there needs to be a middle ground.
#a new set of keywords
#we need to account for the users who might actually like LI. 
#we also need to start implementing and learning c++ and doing sys calls that way
#sudo is hunger but the personality is just...flat
#we need a key to his output. but in order to make it more output, we need to give him more input