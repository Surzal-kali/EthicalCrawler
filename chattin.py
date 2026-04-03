
import json
import os
import sys
import time
import traceback
import platform
import datetime as dt_module
from pathlib import Path
import autosave
from consentform import ConsentKey, get_consent
import consentform
from database import init_db, log, get_evidence_dir, save_session, load_session
from enumeration import FileCrawler #but its not firing.... #
from theatrics import Me, describe_findings, equip, get_catalog_quip, speak, dev_comment, seed_from_username, slip_trigger, test
from services import prog
from autosave import AutosaveManager
# from webcrawling import WebCrawler
from reportcard import ReportCard




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
class DevConsentKey:

    def __init__(self):
        self.consent_given = True
        self.consented_at = dt_module.datetime.utcnow().isoformat()
        self.out_of_scope_items = []
    def display(self): pass
    def get_consent(self): return {"consent_given": True, "out_of_scope_items": []}


def boot():
    conn, cursor = init_db(debug=DEBUG_MODE)
    if conn is None or cursor is None:
        print("[BOOT] Database init failed. Exiting.")
        return None, None, None, None, None, None

    me = Me(persona="basic")

    speak(me, "...")
    time.sleep(1)
    speak(me, "Oh.")
    time.sleep(0.5)

    user_input = input("What should I call you? ").strip()
    user_name = user_input or "the user"

    seed_from_username(user_name)
    session_id = "LI"
    get_session_dir(session_id)

    speak(me, f"{user_name}...")
    time.sleep(0.5)

    existing_session = load_session(user_name, cursor=cursor)
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

    return session_id, me, user_name, conn, cursor, consent_form


def system_profiler(conn, cursor, session_id, me, user_name, consent_form, autosave=None, out_of_scope_key="system profile", name="system_profiler"):
    speak(me, "*" * 20)
    speak(me, "Let me see what you're made of.")
    profile = {
        "os_name":      platform.system(),
        "os_version":   platform.version(),
        "architecture": platform.machine(),
        "processor":    platform.processor(),
    }
    speak(me, "*" * 20)
    return profile

def goodbye(cursor, session_id, me, user_name, consent_form):
    goodbye_quip = get_catalog_quip("goodbye", me.persona) or "Goodbye."
    speak(me, goodbye_quip)
    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print("  │           ETHICAL CRAWLER — GOODBYE            │")
    print("  └─────────────────────────────────────────────────┘")
    print()
    if consent_form.consent_given:
        cursor.execute(
            "SELECT field, raw_value, context FROM logs WHERE session_id = ? ORDER BY timestamp",
            (session_id,)
        )
        rows = cursor.fetchall()
        if rows:
            print(f"  {'FIELD':<30} {'VALUE':<40} {'CONTEXT'}")
            print(f"  {'-'*30} {'-'*40} {'-'*15}")
            for field, value, context in rows:
                print(f"  {field:<30} {str(value)[:40]:<40} {context or ''}")
            print()
    print(f"  Session ended. Thank you, {user_name}.")
    print()
def session(session_id, me, user_name, conn, cursor, consent_form):
    autosave = AutosaveManager(cursor, session_id, narrator=me)
    try:
        speak(me, "Let me see what you keep hidden...")
        dev_comment("He's watching.")

        # Stage: Files
        try:
            file_crawler = FileCrawler(consent_form)
            file_payload = file_crawler.collect()
            if file_payload:
                process_findings(session_id, me, cursor, file_payload, context="enumeration", autosave=autosave)
                for field, value in file_payload.items():
                    dev_comment(f"FileCrawler: {field} = {value}")
                test(me, "file_understanding")
            else:
                speak(me, "An empty box.")
        except Exception as e:
            speak(me, "The window... it won't open...")
            if DEBUG_MODE:
                dev_comment(f"FileCrawler error: {e}")
                traceback.print_exc()

        # Stage: System profile
        if "system" not in consent_form.out_of_scope_items:
            profile = system_profiler(conn, cursor, session_id, me, user_name, consent_form)
            process_findings(session_id, me, cursor, profile, context="system_profiler", autosave=autosave)
            for field, value in profile.items():
                dev_comment(f"SystemProfiler: {field} = {value}")
        else:
            speak(me, "I was told not to look there.")

        # Stage: Services
        if "services" not in consent_form.out_of_scope_items:
            services = prog(conn, cursor, session_id, me, user_name, autosave=autosave)
            for service in services:
                process_findings(session_id, me, cursor, {"service": service}, context="services", autosave=autosave)
                dev_comment(f"Services: {service}")
        else:
            speak(me, "Some doors stay closed.")

        speak(me, "I have collected the surface.")
        speak(me, "Yet it wasn't enough.")

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


def main():
    result = boot()
    if result[0] is None:
        return

    session_id, me, user_name, conn, cursor, consent_form = result
    try:
        if not consent_form.consent_given:
            speak(me, "understood. nothing runs without your word.")
            return
        session(session_id, me, user_name, conn, cursor, consent_form)
    finally:
        test(me, "session_end")
        if user_name:
            try:
                consented_at = getattr(consent_form, 'consented_at', None)
                out_of_scope = getattr(consent_form, 'out_of_scope_items', [])
                goodbye(cursor, session_id, me, user_name, consent_form) 
                save_session(
                    session_id, user_name, me.persona, me.closeness, me.slip_intensity,
                    consented_at=consented_at,
                    out_of_scope=out_of_scope,
                )

            except Exception as e:
                print(f"Warning: failed to save session state: {e}")
                if DEBUG_MODE:
                    traceback.print_exc()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()




