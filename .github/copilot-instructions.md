# Project Guidelines

See README.md for the project overview, narrative tone, and current feature scope.

## Build And Test

- Install dependencies: `pip install -r requirements.txt`
- Run (beginner entry): `python runme.py` — fires dev_forward() then hands off to chattin.main()
- Run (dev iteration, consent bypassed): `python chattin.py` directly — uses DevConsentKey inline
- Run autosave tests: `python test_autosave.py` (12 tests, in-memory SQLite, no interactive prompts)
- Run database tests: `python -m unittest test_db` (schema/init tests, isolated via `$ETHICAL_CRAWLER_DATA_DIR`)
- No CI or linter is configured. Validation is manual or targeted. The main run path blocks on consent input — avoid full end-to-end runs unless the task explicitly needs it.

## Architecture

### Session Lifecycle

```
runme.py → dev_forward() → chattin.main()
  ├─ boot()
  │   ├─ init_db() → SQLite (WAL mode) + Me(persona="basic")
  │   ├─ seed_from_username() → deterministic RNG from MD5(username)
  │   ├─ load_session() → restore persona/closeness/slip_intensity from JSON
  │   ├─ EULA gate: consented_at present → silent DevConsentKey (no form)
  │   │             consented_at absent  → ConsentKey.display() + tk checkbox menu
  │   └─ returns (session_id, me, user_name, conn, cursor, consent_form)
  │
  └─ session()  ← only runs if consent_given=True
      ├─ AutosaveManager(cursor, session_id, narrator=me)
      ├─ FileCrawler.collect() → file picker + metadata payload
      ├─ system_profiler() → OS/hardware flat dict
      ├─ services.prog() → psutil process enumeration
      ├─ WebCrawler.collect_and_log() → link extraction
      ├─ Each stage → process_findings() → log() + equip()
      ├─ autosave.flush(allow_partial=True) in finally block
      └─ save_session() → persist persona/closeness/slip/consented_at/out_of_scope to JSON
```

### Module Responsibilities

| File | Role |
|------|------|
| `runme.py` | Personal forward — dev's note to the user, then hands off to `chattin.main()` |
| `chattin.py` | **Primary entry point** — boot ritual, EULA gate, session lifecycle, stage ordering |
| `LIMain.py` | Legacy orchestration — being superseded by chattin.py, do not extend |
| `database.py` | SQLite schema + PRAGMA, `log()`, `save_session()`, `load_session()`, evidence paths |
| `theatrics.py` | `Me` class (persona state machine), `speak()`, `equip()`, `sudo()`, quip lookup, instability rendering |
| `autosave.py` | `AutosaveManager` — buffered persistence with partial-save + retry |
| `quips.py` | `QUIP_CATALOG` (4 personas), `normalize_quip_key()`, `get_catalog_quip()` |
| `services.py` | `prog()` — psutil process enumeration, placeholder stage |
| `enumeration.py` | `FileCrawler` — Tkinter file picker + metadata extraction |
| `webcrawling.py` | `WebCrawler` — link extraction stub; `robots_txt()` and `crawl_and_enumerate()` are incomplete |
| `consentform.py` | `ConsentKey` — EULA CLI narration + tk terminal-style checkbox menu for out-of-scope |
| `reportcard.py` | `ReportCard` — placeholder for Act III session summary |

### Persona State Machine

`Me.persona` progresses: `"basic"` → `"foothold"` → `"helper"` → `"sudo"`

- Closeness ≥ 85 → escalates to `"helper"`; slip_intensity ≥ 15 → escalates to `"sudo"`
- `"sudo"` voice prepends `[MIMIC]` and uppercases output via `persona_filter()`
- `slip_trigger()` probability includes hotwords: `"root"`, `"secret"`, `"vanessa"` (weight 3.0)

## Response Style

- For any non-trivial logic change, include a brief pseudocode outline **inline before the code** — not as a separate approval step, just as part of the explanation.
- Skip pseudocode for one-liners, rename-only changes, or anything self-evident from the diff.
- If the user says they're stuck or asks to skip ahead, go straight to implementation without the pseudocode preamble.

## Key Conventions

### Stage Contract

New collection stages must return a **flat dict** `{field: value, ...}` and integrate via `process_findings()`:

```python
payload = my_stage.collect()  # returns flat dict
if payload:
    process_findings(session_id, me, cursor, payload, context="my_stage", autosave=autosave)
```

`process_findings()` calls `describe_findings()` (pre-compute quips), then `log()`, then `equip()`. Do not call these three separately unless you have a specific reason.

### Core Function Signatures

```python
# Persist an annotated log entry immediately (commits to SQLite)
log(cursor, session_id, field, raw_value, narrator, context="system_profiler",
    normalized_key=None, quip_text=None)

# Narrator comments on findings; buffers to autosave if provided
equip(narrator, system_info, cursor=None, autosave=None, descriptions=None)
# descriptions = pre-computed {field: {value, normalized_key, quip_text}} from describe_findings()

# AutosaveManager usage pattern
autosave = AutosaveManager(cursor, session_id, narrator=me)
autosave.add("field_name", value, context="stage_name")  # returns False if duplicate
status = autosave.flush(allow_partial=True)               # {saved: [...], failed: [...]}
autosave.retry_failed()                                   # re-attempt failed fields
```

### Narrative Output Functions

Use the right output function for the context:

| Function | When to use |
|----------|-------------|
| `speak(me, message)` | All narrator voice lines (applies instability if slip_intensity ≥ 4) |
| `dev_comment(msg)` | Red `[DEV COMMENT]` — internal debug only, never part of narrator voice |
| `test(me, message)` | DEV MODE — shows persona/closeness/slip state |
| `sudo(me, message)` | Controlled instability beat — bumps slip +1.5, closeness +1 |
| `slip_trigger(me, message)` | Probability-based glitch check before a `speak()` call |

### Quip Catalog

Add new quips to `quips.py` `QUIP_CATALOG` (keyed by persona: `all`, `foothold`, `helper`, `sudo`). Add new field→key mappings to `normalize_quip_key()` via `FIELD_KEYWORDS`. Do not hardcode quip strings inline in stage modules.

### Autosave in Finally Blocks

Always wrap `autosave.flush()` in a `finally` block so partial data is saved even on error:

```python
try:
    # ... collection stages ...
finally:
    autosave.flush(allow_partial=True)
    save_session(...)
```

## Project-Specific Pitfalls

- **Data paths**: Use `get_evidence_dir()` from `database.py`. Override with `$ETHICAL_CRAWLER_DATA_DIR` for test isolation. Never hardcode paths.
- **Consent check in stages**: Call `consent_form.consent_given` and check `consent_form.out_of_scope_items` before collecting — see `FileCrawler.collect()` as the reference implementation.
- **`equip()` signature drift**: The actual signature is `equip(narrator, system_info, cursor=None, autosave=None, descriptions=None)`. The `descriptions` param accepts pre-computed output from `describe_findings()` to avoid redundant quip lookups.
- **Session state is JSON, not SQLite**: `save_session()` / `load_session()` write to `{data_dir}/session_states/{canonical_username}.json`. The SQLite fallback in `load_session()` is a migration path for old data only.
- **`webcrawling.py` and `reportcard.py` are stubs**: `robots_txt()`, `crawl_and_enumerate()`, and `ReportCard` are unimplemented placeholders. Don't treat them as complete.
- **`runme_dev.py` is stale**: The active dev bypass is `DevConsentKey` inline in `chattin.py`. `runme_dev.py` monkey-patches `LIMain.ConsentKey` which is the old path — ignore it.

## Authorization Requirement

- Treat any new enumeration, monitoring, or security-testing behavior as in-scope only when the user has explicit authorization for the target system.
- Do not broaden collection beyond the stated task without the user asking for it.