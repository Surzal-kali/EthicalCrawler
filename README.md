    # LI - Executive Summary

LI is a narrative-driven system enumerator that behaves like a character rather than a plain tool.

Act I (the currently implemented phase) focuses on host profiling with theatrical narration. Future acts are planned for user-facing review and personality rebirth.

## Beginner Entry Point

Use this as your first run path:

- Install dependencies: `pip install -r requirements.txt`
- Start LI: `python runme.py`

`runme.py` is the recommended beginner entry point. It handles intro framing, then forwards into the Act I orchestration flow.

## What LI Does In Act I

- Profiles operating system and hardware basics
- Enumerates common running services/process signals
- Logs findings to SQLite evidence/log tables
- Reacts with persona-driven quips, mood shifts, and instability effects
- Tracks session state across runs via per-user JSON files in the project data folder
- Requires interactive consent before collection continues

## Architecture Overview

- `runme.py`: Beginner-friendly launch path and narrative prelude
- `Chattin.py`: Main orchestration (boot sequence, consent gate, session lifecycle, stage ordering)
- `database.py`: SQLite setup, project data paths, JSON session state load/save, evidence/log handling
- `theatrics.py`: Persona model, normalization, quip logic, rendering, slip mechanics
- `services.py`: Process/service detection stage for Act I
- `autosave.py`: Buffered persistence with retry/partial-save support
- `consentform.py`: Consent workflow and out-of-scope capture
- `quips.py`: Quip catalog and key normalization helpers

## Current Status

Act I is functional but still evolving.

- Implemented: boot ritual, consent gate, profiling, service stage, quip/mood/slip systems, persistence
- In progress: scanner modularization, deeper stages, schema cleanup, stronger act boundaries
- Planned: Act II (user data review flow), Act III (rebirth/profile synthesis)

## Practical Notes

- The main flow is interactive and blocks on consent input.
- Validation is currently targeted/manual rather than CI-driven.
- Session internals currently favor debug/testing transparency and may be refined as the project stabilizes.

## Why This Exists

LI is an experiment at the intersection of:

- system enumeration
- persistent state
- narrative design
- persona evolution
- ethical tension in tooling

It is intentionally part tool, part character, and part story engine.

