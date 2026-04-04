import json
import os
import sys
import threading
import time
import traceback
import platform
import datetime as dt_module
from pathlib import Path
import autosave
from consentform import ConsentKey, get_consent
import consentform 
from database import SessionStore, save_session, load_session, get_evidence_dir, canonical_username
from enumeration import FileCrawler #but its not firing.... #
from reportcard import report, ReportCard
from theatrics import Me, describe_findings, equip, get_catalog_quip, speak, dev_comment, seed_from_username, slip_trigger, test
from services import prog
from autosave import AutosaveManager
# from webcrawling import WebCrawler
from webcrawling import WebCrawler
from digestion import Digestion
#:) ill brb i need to save that
#so how long will the payload printing take? 
""" Ethical Crawler: A personal data enumerator and narrator."""
DEBUG_MODE = "--debug" in sys.argv or os.getenv("ETHICAL_CRAWLER_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}
SLIP_DECAY_PER_DAY = 0.5
MIN_SLIP_INTENSITY = 1.0



def decay_slip_intensity(saved_intensity, last_accessed, decay_per_day=SLIP_DECAY_PER_DAY, floor=MIN_SLIP_INTENSITY):
    """Decay slip intensity by time-away so long absences cool instability. takes saved_intensity, last_accessed timestamp, optional decay_per_day rate, and optional floor value as parameters. Returns the decayed slip intensity."""
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


def process_findings(session_id, me, store, payload, context, autosave=None, user_name=None):
    """Log and narrate a payload through one shared orchestration path."""
    if not payload:
        return
#well theres the problem 
    descriptions = describe_findings(me, payload)
    for field, detail in descriptions.items():
        store.add_log(
            field,
            detail["value"],
            context=context,
            persona=me.persona,
            normalized_key=detail["normalized_key"],
            quip_text=detail.get("quip_text"),
            user_name=user_name,


        )
        #where is the main problem, he keeps saying its an empty box :( 

    equip(me, payload, autosave=autosave, descriptions=descriptions)


class DevConsentKey:
    """Development consent key that bypasses actual consent for testing purposes. Always returns consent given with no out-of-scope items."""

    def __init__(self):
        self.consent_given = True
        self.consented_at = dt_module.datetime.utcnow().isoformat()
        self.out_of_scope_items = []
    def display(self): pass
    def get_consent(self): return {"consent_given": True, "out_of_scope_items": []}


def boot():
    """Boot the Ethical Crawler, handling user greeting, session resumption, and consent management. Returns session_id, me, user_name, store, and consent_form for use in the main session orchestration."""
    me = Me(persona="basic")

    speak(me, "...")
    time.sleep(1)
    speak(me, "Oh.")
    time.sleep(0.5)

    user_input = input("What should I call you? ").strip()
    try:
        user_name = user_input if user_input else "the user"
    except Exception:
        user_name = "the user"
    seed_from_username(user_name)
    session_id = "LI"
    get_session_dir(session_id)

    store = SessionStore(session_id, user_name)

    speak(me, f"{user_name}...")
    time.sleep(0.5)

    existing_session = load_session(user_name)
    if existing_session:
        me.persona = existing_session["persona"]
        me.slip_intensity = decay_slip_intensity(
            existing_session["slip_intensity"],
            existing_session["last_accessed"],
        )
        me.closeness = existing_session["closeness"]
        dev_comment(f"Session resumed — persona={me.persona} closeness={me.closeness} slip={me.slip_intensity}")
        speak(me, f"{user_name.upper()}… You're back.")
    else:
        dev_comment("No prior session — starting fresh.")
        speak(me, f"{user_name.upper()}… Interesting.")

    me.user_name = user_name

    if existing_session and existing_session.get("consented_at"):
        consent_form = DevConsentKey()
        dev_comment("Returning user — consent on file, skipping form.")
    else:
        consent_form = ConsentKey() if not DEBUG_MODE else DevConsentKey()
        consent_form.display()
        consent_form.get_consent()
        if DEBUG_MODE:
            dev_comment("Consent bypassed (dev mode)")

    return session_id, me, user_name, store, consent_form


def system_profiler(session_id, me, user_name, consent_form, autosave=None, out_of_scope_key="system profile", name="system_profiler"):
    """Collect system profile information, including OS name, version, architecture, and processor. takes database connection, cursor, session_id, me, user_name, optional consent_form, optional autosave manager, out_of_scope_key, and name as parameters. Returns a dictionary with the collected system profile data."""
    speak(me, "*" * 20)
    speak(me, "Let me see what you're made of.")
    profile = {
        "os_name":      platform.system(),
        "os_version":   platform.version(),
        "architecture": platform.machine(),
        "processor":    platform.processor(),
        "platform":     platform.platform(),   
        "python_version": platform.python_version(), 
        "timezone":     time.tzname[0], #there its done
        "cores": os.cpu_count(),
        "thread_count": threading.active_count(),
    }
    speak(me, "*" * 20)
    return profile

def goodbye(store, session_id, me, user_name, consent_form, consented_at=None, out_of_scope=None, prog=None, save_session_func=None, report_func=None, report_card=None):
    """Demo exit for report card findings. takes store, session_id, me, user_name, and consent_form, consented_at, out_of_scope, prog, save_session_func, report_func, and report_card as parameters. Returns nothing."""
    goodbye_quip = "Goodbye." #lets take it out for now bc we need to work on digestion and theatrics first, but we can bring it back for flavor later.
    speak(me, goodbye_quip)
    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │           ETHICAL CRAWLER — GOODBYE            │")
    print("  └─────────────────────────────────────────────────┘")
    print()
    if consent_form.consent_given:
        rows = store.get_log()
        if rows:
            print(f"  {'FIELD':<30} {'VALUE':<40} {'CONTEXT'}")
            print(f"  {'-'*30} {'-'*40} {'-'*15}")
            for row in rows:
                print(f"  {row['field']:<30} {str(row['raw_value'])[:40]:<40} {row.get('context') or ''}")
            print()
    print(f"  Session ended. Thank you, {user_name}.")
    print()
    store.close()
#this needs a rewrite. #but it also needs testing with the report card, and new digestion scripting, and more quips. #yeth



    #the main orchestration
    #ready to compose? ill take that as a yes
    #think thats it. 
def session(session_id, me, user_name, store, consent_form):
    """Main session orchestration for the Ethical Crawler. Handles the flow of enumeration, narration, and logging while respecting user consent and out-of-scope boundaries. takes session_id, me, user_name, store, and consent_form as parameters. Returns nothing."""
    autosave = AutosaveManager(store, session_id, narrator=me, user_name=user_name)
    try:
        speak(me, "Let me see what you keep hidden...")
        dev_comment("She's watching.")
        time.sleep(1)

        # Stage: System
        if "system" not in consent_form.out_of_scope_items:
            profile = system_profiler(session_id, me, user_name, consent_form)
            process_findings(session_id, me, store, profile, context="system_profiler", autosave=autosave, user_name=user_name)
            time.sleep(1)
        else:
            speak(me, "I was told not to look there.")
            time.sleep(1)

        # Stage: Files
        if "files" not in consent_form.out_of_scope_items:
            try:
                file_crawler = FileCrawler(consent_form)
                file_payload = file_crawler.collect(cores=os.cpu_count(), frequency=(threading.active_count() or 1) * 2, autosave=autosave)
                if file_payload:
                    process_findings(session_id, me, store, file_payload, context="enumeration", autosave=autosave, user_name=user_name)
                    test(me, "file_enumeration")
                else:
                    speak(me, "An empty box.")
            except Exception as e:
                speak(me, "The window... it won't open...")
                if DEBUG_MODE:
                    dev_comment(f"FileCrawler error: {e}")
                    traceback.print_exc()
        else:
            speak(me, "Files are off the table.")
            time.sleep(1)
        # Stage: Web
        if "web" not in consent_form.out_of_scope_items:
            try:
                webcrawler = WebCrawler(consent_form)
                web_payload = webcrawler.collect_and_log(store, session_id, me, autosave=autosave)
                if web_payload:
                    process_findings(session_id, me, store, {"web_links": web_payload}, context="web_crawling", autosave=autosave, user_name=user_name)
                    test(me, "web_crawling")
            except Exception as e:
                speak(me, "The network went quiet.")
                if DEBUG_MODE:
                    dev_comment(f"WebCrawler error: {e}")
                    traceback.print_exc()
        else:
            speak(me, "You told me to stay off the web.")
            time.sleep(1)

        # Stage: Services
        if "services" not in consent_form.out_of_scope_items:
            services = prog(store, session_id, me, user_name, autosave=autosave)
            for service in services:
                process_findings(session_id, me, store, {"service": service}, context="services", autosave=autosave, user_name=user_name)
        else:
            speak(me, "Some doors stay closed.")
            time.sleep(1)

        speak(me, "I have collected the surface.")
        speak(me, "Yet it wasn't enough.")
        time.sleep(1)
        #Stage: Digestion
        digestion = Digestion(consent_form)
        digested_payload = digestion.digest(store, session_id, me, autosave=autosave)
        if digested_payload:
            process_findings(session_id, me, store, digested_payload, context="digestion", autosave=autosave, user_name=user_name)
        else:
            speak(me, "I tried to understand, but it's beyond me.")
            time.sleep(1)
    except Exception as e:
        speak(me, "I can't see. Something is wrong.")
        print(f"[ERROR] Session error: {type(e).__name__}: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
    finally:
        save_status = autosave.flush(allow_partial=True)
        if save_status["failed"]:
            dev_comment(f"Autosave partial failure: {save_status['failed']}")
            retry_status = autosave.retry_failed()
            if retry_status["failed"]:
                dev_comment(f"Autosave retry failure: {retry_status['failed']}")
            else:
                dev_comment("Autosave retry succeeded.")
        else:
            dev_comment("Autosave flush succeeded.")

def main():
    """Main entry point for the Ethical Crawler. Handles booting, session orchestration, and graceful shutdown with report card findings. Returns nothing."""
    session_id, me, user_name, store, consent_form = boot()
    try:
        if not consent_form.consent_given:
            speak(me, "understood. nothing runs without your word.")
            return
        session(session_id, me, user_name, store, consent_form)
    finally:
        test(me, "session_end")
        try:
            consented_at = getattr(consent_form, 'consented_at', None)
            out_of_scope = getattr(consent_form, 'out_of_scope_items', [])
            report_card = ReportCard(consent_form).generate(store, session_id, me)
            # legacy code goodbye(store, session_id, me, user_name, consent_form, consented_at=consented_at, out_of_scope=out_of_scope, report_card=report_card)
        except Exception as e:
            dev_comment(f"Error during goodbye sequence: {e}")
            if DEBUG_MODE:
                traceback.print_exc()
            save_session(session_id, user_name, me.persona, me.closeness, me.slip_intensity, consented_at=consented_at, out_of_scope=out_of_scope)
    store.close()


if __name__ == "__main__":
    main()




