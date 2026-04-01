# Project Guidelines

See README.md for the project overview, narrative tone, and current feature scope.

## Build And Test

- Install dependencies with `pip install -r requirements.txt`.
- Run the project with `python runme.py`.
- There is no automated test suite yet. Prefer targeted validation over broad refactors, and note when verification is manual or blocked by the interactive consent flow.

## Architecture

- VanessaPFinal.py is the main orchestration layer: boot sequence, consent flow, session lifecycle, and stage ordering.
- database.py owns SQLite initialization, cleanup, and narrator-aware logging.
- theatrics.py owns persona state, rendering, normalization, and quip generation.
- services.py and similar modules should behave like collection stages and integrate with the session flow rather than duplicating boot or narration logic.

## Conventions

- Preserve the narrative CLI style. Technical data collection is wrapped in theatrical output, so keep user-facing messages consistent with the existing voice.
- When adding a new collection stage, keep the flow consistent: collect data, log findings through `log(...)`, then pass a narrator-friendly summary into `equip(...)`.
- Keep changes small and local. This repository is still evolving, and several collection stages are placeholders.
- Prefer extending existing modules over introducing new abstractions unless repeated patterns justify it.

## Project-Specific Pitfalls

- The codebase currently hardcodes `/tmp/` paths in database.py and the boot flow. Do not assume Windows-safe paths unless you are explicitly fixing that behavior.
- The main run path is interactive and requires consent input. Avoid turning routine validation into full end-to-end runs unless the task actually needs it.
- `equip(narrator, system_info, cursor=None, autosave=None)` expects a flat mapping of fields to values. Pass the session `autosave` instance to buffer data automatically. Return shapes from new stages should stay compatible unless you also update the narration layer.

## Authorization Requirement

- Treat any new enumeration, monitoring, or security-testing behavior as in-scope only when the user has explicit authorization for the target system.
- Do not broaden collection beyond the stated task without the user asking for it.