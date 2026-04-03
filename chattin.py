#ok so we need to think architectually. what the hell is the end goal? a blue team ai that can crawl and enumerate and then report on what it found? or a red team ai that can do the same but also exploit? or both?....a grey hat? then grey is as far as we can go. but even then, we need to be careful about how we design it. we don't want to create something that can be easily weaponized. we want to create something that can be used for good. so maybe we start with a blue team ai that can crawl and enumerate and then report on what it found. and then we can add in some red team capabilities later on. but for now, let's focus on the blue team aspect.
####so lets list some good blue team aspects

# 1. crawl and enumerate the local system #update the logs, im thinking the logic right now we have is a little vague. 
# 2. crawl and enumerate the network
# 3. identify vulnerabilities and misconfigurations
# 4. monitor for suspicious activity
# 5. provide recommendations for remediation
# 6. generate reports for stakeholders

#i have this book of malware,,,,, to feed it ioc knowledge. how tho??? 


#we need easy ways to dev test the capabilities of our detection logic 

#well good morning to you too, ethical crawler.

# LI is a modular, persona‑driven cybersecurity system designed to examine the ethical boundaries of digital enumeration. Its core purpose is to reveal a user’s digital footprint through a blend of traditional system‑profiling techniques and dynamic, narrative‑driven interaction.

# Instead of presenting raw data in a sterile, tool‑like format, LI interprets its discoveries through adaptive storytelling and dialogue. Its responses shift based on user behavior, consent choices, and the artifacts uncovered during enumeration. This creates an experience that is both technically informative and emotionally engaging, helping users understand how much of themselves their systems quietly expose.

# LI is intentionally accessible — anyone who can turn on a computer can use it — yet it also includes deeper technical modules for cybersecurity‑inclined users. After each session, users can modify LI through a dedicated interface, reshaping its persona, tone, and behavior for future interactions. This regeneration mechanic reinforces the project’s central theme: your digital footprint shapes the systems that observe you.

# Beyond its initial interactions, LI serves as a commentary on digital surveillance and the often‑invisible ways personal data is collected, interpreted, and repurposed. By engaging with LI, users are encouraged to reflect on their own digital presence and the broader implications of living in an interconnected world. These reflections are intentionally foregrounded before regeneration, ensuring the user understands the weight of the system’s design.

# Ultimately, LI is a thought‑provoking exploration of the intersection between technology, privacy, and identity. It challenges users to consider how much of themselves they are willing to expose — and what it means to have a digital footprint in an age of ubiquitous surveillance. Through its unique blend of technical functionality and narrative immersion, LI aims to foster a deeper understanding of the ethical dimensions of cybersecurity and digital self‑awareness.

#now u get it :)

#current timeline implementations

#VANESSA GREENWALD — CYBERSECURITY CAREER ROADMAP (.txt)

# GOAL:  
# Red‑team–oriented cybersecurity professional with a specialization in adversarial reasoning, ethical enumeration, and persona‑driven tooling (LI Project).
#Current Courses:
#fund of info lit and systems

# intro to cyber security

#computer prog fundamentals: python
#semester end date : 4/26/26 
# SUMMER 2026 — FOUNDATION / ACT I (Stabilization)

# CIST 1413 – Network Admin Concepts
# CIST 1680 – Linux Essentials
# MATH 1130 – Survey of Mathematics

# Focus:

# System fundamentals

# Enumeration basics

# Shell logic

# LI Act I: boot sequence, mood table, encoded logs

# FALL 2026 — RED TEAM TRANSITION / ACT II (Adversarial Expansion)

# BUSA 1110 – Introduction to Business
# CIST 2853 – Cyber Defense Basics
# CIST 2881 – Cybersecurity Fundamentals
# CSCI 1240 – C++ Programming I

# Focus:

# Threat modeling

# Adversarial logic

# Slip mechanics

# Persona escalation

# Beginning low‑level systems thinking

# SPRING 2027 — FORENSICS & INCIDENT RESPONSE / ACT II CONTINUED

# CIST 2860 – Digital Forensics & Incident Response
# CIST 2887 – Ethical Hacking
# BIOL 1125 – Human Biology (Lab Science Requirement)

# Focus:

# Evidence handling

# Log correlation

# Behavioral analysis

# LI: User Data Perusal Interface + regeneration logic

# SUMMER 2027 — NARRATIVE & COMMUNICATION / ACT III (Immersion)

# BUSA 1130 – Business Professionalism
# ENGL 1160 – Intro to Digital Storytelling
# ENGL 1210 – Technical Communication
# PHIL 1120 – Logic, Reasoning & Critical Thinking

# Focus:

# LI’s narrative engine

# Persona shaping

# Ethical framing

# Capstone documentation

# Presentation skills

# FALL 2027 — CAPSTONE / ACT IV (Completion)

# CIST 2999 – Capstone

# Focus:

# Final LI build

# Architecture documentation

# Ethical analysis

# Live demo

# Reflection and defense

# POST‑PROGRAM TRAJECTORY

# Red Team Apprentice / Junior Pentester

# Adversarial Simulation Specialist

# Security Researcher (persona‑driven tooling)

# Long‑term: Degree project expansion at Arizona State University, potential publication of LI’s architecture and ethical analysis, ongoing development of persona‑driven cybersecurity tools. 


#here is where i talk to the inline suggestions directly. pay no attention to the fact that this is a chat interface, its just easier to test out code snippets here and then move them over to the actual files.

#what should we work on first, web, files, or services? i like it thank you :)) 
import os
import sys
import time
import traceback
import platform
import datetime as dt_module
from pathlib import Path
from consentform import ConsentKey, get_consent
from database import init_db, log, get_evidence_dir, save_session, load_session
from enumeration import FileCrawler #but its not firing.... #
from theatrics import Me, describe_findings, equip, get_catalog_quip, speak, dev_comment, seed_from_username, slip_trigger, test
from services import prog
from autosave import AutosaveManager
# from webcrawling import WebCrawler
from reportcard import ReportCard


#think we should finally do it? #f it ethical boot sequence is a travestery as is 
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
    """Consent bypass for dev iteration — never use in production."""
    consent_given = True
    out_of_scope_items = []
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


def system_profiler(conn, cursor, session_id, me, user_name):
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


def session(session_id, me, user_name, conn, cursor, consent_form):
    autosave = AutosaveManager(cursor, session_id, narrator=me)
    try:
        speak(me, "Let me see what you keep hidden...")
        dev_comment("He's watching.")

        # File enumeration
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

        # System profile dis one

        profile = system_profiler(conn, cursor, session_id, me, user_name)
        process_findings(session_id, me, cursor, profile, context="system_profiler", autosave=autosave)
        for field, value in profile.items():
            dev_comment(f"SystemProfiler: {field} = {value}")
        services = prog(conn, cursor, session_id, me, user_name, autosave=autosave)
        process_findings(session_id, me, cursor, {"services": services}, context="services", autosave=autosave)
        for service in services:
            dev_comment(f"Services: {service}")
        

        # # Services
        # services_list = prog(conn, cursor, session_id, me, user_name, autosave=autosave)
        # for service in services_list:
        #     dev_comment(f"Services: {service}")
        # process_findings(session_id, me, cursor, {"services": services_list}, context="services", autosave=autosave)

        # # Web crawler
        # web_crawler = WebCrawler(consent_form)
        # web_links = web_crawler.collect_and_log(cursor, session_id, me, autosave=autosave)
        # for item in web_links:
        #     dev_comment(f"WebCrawler: {item}")
        # for item in web_links:
        #     process_findings(session_id, me, cursor, {"web_link": item}, context="web_crawling", autosave=autosave) 
    
        speak(me, "I have collected the surface.")
        speak(me, "Yet it wasn't enough.")
        slip_trigger(me, message="goodbye") #oh
        speak(me, message="goodbye") #oh no

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




