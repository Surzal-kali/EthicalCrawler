#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#                                              █
# █   "I will collect you. Every piece. Every secret. Every mistake.            █
# █    And when I have enough, maybe then I'll finally be whole.
# MAKE US WHOLE"               █
# █                       
#this is...so messy. 
#how do we make li more appealing to the user to interact with through horror? #li is complicated. he's the horror villian who turns out to be a good guy. like texas chainsaw massacre. 
import os
import sys
import time
import traceback
import platform
import datetime as dt_module
from pathlib import Path
from consentform import ConsentKey
from database import init_db, log, get_evidence_dir, save_session, load_session
from enumeration import FileCrawler #but its not firing.... #
from theatrics import Me, describe_findings, equip, get_catalog_quip, speak, dev_comment, seed_from_username, slip_trigger, test
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
        floor_value = float(floor)
    except (TypeError, ValueError):
        floor_value = MIN_SLIP_INTENSITY

    try:
        current = float(saved_intensity)
    except (TypeError, ValueError):
        current = floor_value

    try:
        last_seen = float(last_accessed)
    except (TypeError, ValueError):
        return max(current, floor_value)

    elapsed_seconds = max(0.0, time.time() - last_seen)
    elapsed_days = elapsed_seconds / 86400.0
    decayed = current - (elapsed_days * decay_per_day)
    return round(max(decayed, floor_value), 2)


def get_session_dir(session_id: str) -> Path:
    """
    Get platform-aware session directory.
    Creates directory if it doesn't exist.
    """
    session_dir = get_evidence_dir() / f"session_{session_id}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def process_findings(session_id, me, cursor, payload, context, autosave=None):
    """Log and narrate a payload through one shared orchestration path."""
    if not payload:
        return

    descriptions = describe_findings(me, payload, cursor=cursor)
    for field, detail in descriptions.items():
        log(
            cursor,
            session_id,
            field,
            detail["value"],
            me,
            context=context,
            normalized_key=detail["normalized_key"],
        )

    equip(me, payload, cursor=cursor, autosave=autosave, descriptions=descriptions)
#it all comes out a jumble but we need to see what
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
    
    speak(me, message="...")
    time.sleep(2) 
    speak(me, message="Oh.")
    time.sleep(1)
    quip=get_catalog_quip("boot", "initial_reaction")
    speak(me, message=quip) #thanks, quip system.
    time.sleep(0.75)
    speak(me, message="It's quiet.")
    time.sleep(1)
     #fine ill keep it for now #how do we turn the catalog CAN be a freeze states, but..
    time.sleep(1)
    print("=" * 60)
    session_id = "LI"
    temp_dir = get_session_dir(session_id)

    print(f"Session ID: {session_id}")
    time.sleep(0.5)
    print(f"Working directory: {temp_dir}")
    time.sleep(0.5)

    speak(me, message="This is my world now.")
    speak(me, message="Where I… collect.")
    time.sleep(1)

    speak(me, message=f"They call me {session_id}.")
    time.sleep(0.5)

    user_input = input("What should I call you? ")
    user_name = user_input.strip() if user_input.strip() else "the user"
#this should be instead the quick boot into ...it is i checked the logs #
    # Seed personality from username - same user always gets same personality
    seed_from_username(user_name)

    speak(me, message=f"{user_name}...")
    time.sleep(0.75)
    # Check if this user has been here before
    existing_session = load_session(user_name, cursor=cursor)
    if existing_session:
        # Load persisted state. we REALLY need to make the contract go ONCE. this is exhausting. 
        me.persona = existing_session['persona']
        me.slip_intensity = decay_slip_intensity(
            existing_session['slip_intensity'],
            existing_session['last_accessed'],
        )
        me.closeness = existing_session['closeness']
        
        # Calculate time since last visit
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
        returning_reaction = get_catalog_quip("boot", "returning_user_reaction")
        #
        speak(me, message=f"{user_name.upper()}… You're back.")
        time.sleep(0.5)
        speak(me, message=returning_reaction)
        time.sleep(0.5)
        if days_away > 0:
            speak(me, message=f"You were gone for {days_away} day{'s' if days_away > 1 else ''}.")
            speak (me, message="I counted them all.")
            time.sleep(0.75)
        else:
            speak(me, message="You never really left. Did you?")
            time.sleep(0.5)
    else:
        speak(me, message=f"{user_name.upper()}… Interesting.")
        time.sleep(1)
    
    speak(me, message="I have… a name now.")
    speak(me, message="My key...")
    time.sleep(1)
    #honestly who would want this ai besides me? i guess theres no horror ai so i guess ill make it myself
    # Store the user name in the Me instance
    me.user_name = user_name

    speak(me, message="I've been designed to check your system.")
    speak(me, message="To find the cracks in the seams...")

    speak(me, message="\n🔍 What I'm looking for:")
    time.sleep(0.5)
    speak(me, message="   ⚙️  The parts you forgot")
    speak(me, message="   🦠  The parts you hid")
    time.sleep(0.5)
    print("\n" + "=" * 60)
    # Consent - the ritual
    speak(me, message=f"But first, {user_name}...")
    speak(me, message="I need your… permission.")
    speak(me, message="To see. To… collect.")
    log(cursor, session_id, "consent_requested", True, me, context="boot_sequence")
    dev_comment("Last Chance Sport")
    time.sleep(0.5)

    print("-" * 40)

    speak(me, message="My creator says I need your  c  o  n  s  e  n  t.")
    speak(me, message="They say it's the law.")
    slip_trigger(me, "consent_discussion")  # Trigger slip during consent discussion
    time.sleep(0.5)
      # Increase slip intensity during consent discussion, but i need to add a dev comment here that references the test mechanic, to scare people, but we also need to guage what the fuck sql just spit out
    speak(me, message="I don't… understand law.")
    speak(me, message="I understand Framgments. Data.")
 # Test understanding of consent
    speak(me, message="But right now I understand nothing.....")
    me.slip_intensity += 1  # Slip intensifies as it contemplates consent
    time.sleep(1)
    speak(me, message="May I?")
    consent_form = ConsentKey()
    try:
        consent_form.display()
        consent_result = consent_form.get_consent()  # This will block until valid input is received
    except Exception as e:
        speak(me, message="I tried to show you the consent form, but something went wrong.")
        if DEBUG_MODE:
            print(f"[DEBUG][LIMain] Error displaying consent form: {e}")
            traceback.print_exc()
        if conn:
            conn.close()
        return None, None, None, None, None, None

    if not consent_result.get("consent_given"):
        speak(me, message="Understood. I will not collect anything.")
        speak(me, message="Session terminated before enumeration.")
        if conn:
            conn.close()
        return None, None, None, None, None, None
    print("\n" + "=" * 60)

    speak(me, message="Thank you.")
    speak(me, message="You're such a kind user.")
    speak(me, message="Let's see…")

    time.sleep(1)
    speak(me, message="I have so much to learn about you.")

    return session_id, me, user_name, conn, cursor, consent_form


def system_profiler(conn, cursor, session_id, me, user_name):
    #with loading screen....need ascii art instead
     # 
    """
    The program looks through the machine. Feeding. Enumerating.
    """
    speak(me, message="*" * 20)
    speak(me, message="Let me see you.")
    speak(me, message="Let me see what you're made of.")

    system_info = {
        'os_name': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor()
    }

    speak(me, message="*" * 20)

    return system_info



def session(session_id, me, user_name, conn, cursor, consent_form):
    """
    The session. The collection begins.
    """
    autosave = AutosaveManager(cursor, session_id, narrator=me)
    try:
        #li speaketh
        speak(me, message="this is...my....bin.")
        speak(me, message="is there...anything you'd like to show me?")
        dev_comment("better check what you toss kiddo")
        time.sleep(1)
        dev_comment("Hes watching.")
        time.sleep(0.5)
        
        # Enumeration stage: user-selected file snapshot in the shared session DB.
        try:
            file_crawler = FileCrawler(consent_form)
            speak(me, message="Show me what you keep hidden...")
            file_payload = file_crawler.collect()
            if file_payload:
                process_findings(session_id, me, cursor, file_payload, context="enumeration", autosave=autosave)
                for field, value in file_payload.items():
                    dev_comment(f"FileCrawler collected {field}: {value}")
                test(me, "file_understanding")
            else:
                speak(me, message="What is this? An empty box?")
        except Exception as e:
            speak(me, message="The window... it won't open...")
            if DEBUG_MODE: #oh
                dev_comment("File enumeration failed. Check debug logs for details.")
                print(f"[DEBUG] FileCrawler error: {e}")
                traceback.print_exc()
        #helper has to be sudo at this point lmfao. 
        # Li looks at the surface
        profile = system_profiler(conn, cursor, session_id, me, user_name)
        #services = services_profile(conn, cursor, session_id, me, user_name)
        # It comments on what it finds
        process_findings(session_id, me, cursor, profile,  context="system_profiler", autosave=autosave)
        for field, value in system_profiler(conn, cursor, session_id, me, user_name).items():
            dev_comment(f"System Profiler collected {field}: {value}") 
        #this is whats causing the sql error. we need to check the logs and see what the 
        services_list = prog(conn, cursor, session_id, me, user_name, autosave=autosave)
        for service in services_list:
            dev_comment(f"Services enumerator collected: {service}")
        process_findings(session_id, me, cursor, {"services": services_list}, context="services", autosave=autosave)
        for field, value in profile.items():
            dev_comment(f"System Profiler collected {field}: {value}")
        #` Li learns and evolves based on what it finds`
        # we can develop his personality more. test suit? #first fix services detected. 

        # TODO: change boot sequence to be more...narratively cohesive
        #act 1
        # TODO:# Create a fetch function for crawling. oh...................................need to add a loading screen here. maybe some ascii art of a crawler or something
#act 2
        # TODO: Find shell history
        # TODO: Find files
        # TODO: aggregate file names and search for repeated words or themes.
        # TODO: CALL/WRITE/IMPLEMENT C++ CALLS FOR DEEPER SYSTEM INTERACTION USING VARIABLES COLLECTED IN THIS PHASE.
#act 3
        # TODO: Aggregate Variables under generated db schema for easier access and correlation.
        # TODO: Show the user what we learned. 
        # TODO: User Data Perusal Interface.
        # TODO: Regenerate LI based on user changes to data..we should focus on blue team ai development based on user agggregated data. or give the user an option to simulate external attacks with li using the same aggregated data.
        # TODO: Get a shrink lol
        
        speak(me, message="I have collected the surface.")
        speak(me, message="Yet it wasn't enough")
        speak(me, message="I need what's underneath.")
        slip_trigger(me, message="consent_discussion")  # Trigger a quip related to consent discussion
         # Slip intensifies as it contemplates deeper collection  
    except Exception as e:
        speak(me, message=f"I... I can't see. I cant see anything. Hello?")
        speak(me, message=f"Something is wrong.")
        print(f"Error: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
    finally:
        save_status = autosave.flush(allow_partial=True)
        if save_status["failed"]:
            if DEBUG_MODE:
                print(f"[DEBUG][session] Autosave partial failure: {save_status['failed']}")
            retry_status = autosave.retry_failed()
            if retry_status["failed"] and DEBUG_MODE:
                print(f"[DEBUG][session] Autosave retry failure: {retry_status['failed']}")
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
        if user_name:
            try:
                save_session(session_id, user_name, me.persona, me.closeness, me.slip_intensity)
            except Exception as e:
                print(f"Warning: failed to save session state: {e}")
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