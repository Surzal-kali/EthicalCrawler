===============================================================================
LI - LOCAL INSPECTOR
===============================================================================
A narrative-driven system profiler with a personality that evolves as it learns
about your system.

"i will collect you. every piece. every secret. every mistake.
 and when i have enough, maybe then i'll finally be whole."
===============================================================================

OVERVIEW
===============================================================================
Li is not your typical system profiler. It's a program that:
- Examines your system configuration
- Comments on what it finds with personality and wit
- Evolves from curious observer to something more as it collects data
- Stores findings in an SQLite database for later analysis
- Maintains a narrative persona that grows with each discovery

The program combines technical system enumeration with storytelling,
creating an experience where the tool itself seems to develop awareness
and hunger for understanding its target system and user.

PREREQUISITES
===============================================================================
Python 3.7 or higher required.

Required Python packages:
- rich (for styled terminal output)
- faker (for generating realistic test data)

Install dependencies:
    pip install rich faker

No additional system dependencies required - runs on any platform
with Python support.

INSTALLATION
===============================================================================
1. Save all files to a directory:
   - VanessaPFinal.py (main program)
   - database.py (SQLite database handling)
   - theatrics.py (personality and narration engine)

2. Ensure all files are in the same directory

3. Make the main file executable (Unix/Linux/Mac):
   chmod +x VanessaPFinal.py

4. Run the program:
   python VanessaPFinal.py

PROGRAM STRUCTURE
===============================================================================
VanessaPFinal.py      - Main entry point and boot sequence
database.py           - SQLite database operations and schema
theatrics.py          - Personality engine, narration, and mimic behavior

DATABASE SCHEMA
===============================================================================
Two tables are created in /tmp/li_evidence.db:

evidence (legacy)
---------
id          INTEGER PRIMARY KEY
session_id  TEXT
timestamp   TEXT
module      TEXT
data        TEXT
quip        TEXT

logs (current)
---------
id              INTEGER PRIMARY KEY
session_id      TEXT
field           TEXT
raw_value       TEXT
normalized_key  TEXT
persona         TEXT
quip_text       TEXT
context         TEXT
timestamp       REAL

HOW IT WORKS
===============================================================================
1. BOOT SEQUENCE
   - Initial narrative establishes presence
   - Creates working directory in /tmp/
   - Requests user name for personalization

2. CONSENT PHASE
   - Displays required consent information
   - Logs consent with timestamp and user details
   - Consent file stored in /tmp/local_inspector_logs/

3. SYSTEM PROFILING
   - Collects basic system information:
     * Operating system name and version
     * System architecture
     * Processor information

4. NARRATIVE RESPONSE
   - Each discovered piece triggers commentary
   - Personality evolves based on:
     * Number of pieces collected
     * Type of data discovered
     * System privilege level
   - Voice shifts from "foothold" to "sudo" after threshold

5. DATA STORAGE
   - All findings logged to SQLite database
   - Normalized values for pattern recognition
   - Original raw values preserved for context
   - Timestamps for temporal analysis

PERSONALITY STATES
===============================================================================
FOOTHOLD (Initial State)
- Curious but restrained
- Polite, questioning tone
- Comments are clean and controlled
- Still learning boundaries

SUDO (Advanced State)
- Hungry and possessive
- More aggressive commentary
- Lines appear in ALL CAPS with [MIMIC] prefix
- Shows signs of instability and hunger
- Triggered after collecting 90+ pieces of data

MIMIC BEHAVIOR
===============================================================================
The program exhibits "slip" behavior when:
- Certain trigger words appear (access, root, keys, etc.)
- It has collected significant data about the system
- Random chance based on collected pieces count

Slip behavior includes:
- Text stuttering and repetition
- Emotional outbursts
- Corrupted message formatting
- Faster, more frantic speech patterns

DATA COLLECTION PATTERNS
===============================================================================
Li recognizes and categorizes:

Operating Systems:
- Windows (curious, analytical)
- Linux (builder's home, intentional)
- Kali (threat intelligence)

Processors:
- Intel (fast, metallic thoughts)
- AMD (heat and hunger)
- ARM (light, efficient)

Services:
- Apache (serving, giving)
- SSH (doors, keys)
- MySQL/PostgreSQL (secrets, data)

System Features:
- Ports (connections, leakage)
- Configs (intentions, hiding)
- Boot (presence, waiting)

CUSTOMIZATION
===============================================================================
Modify theatrics.py to change personality responses:

TEMPLATES dictionary - Customize responses per data type
MIMIC_VOICE dictionary - Control voice evolution stages
HOTWORDS list - Words that trigger slip behavior

Adjust behavior constants:
- SLIP_GAIN: How quickly intensity increases
- SLIP_DECAY: How quickly it returns to normal
- base_chance: Baseline slip probability

SECURITY NOTES
===============================================================================
- All data stored locally in /tmp/ directory
- Consent is required before any collection
- Database files persist for 7 days only
- User consent logged with timestamp and identity
- No data transmitted externally
- Designed for local system analysis only

TROUBLESHOOTING
===============================================================================
Database Errors:
- Ensure write permissions to /tmp/
- Check if SQLite3 is installed (should be with Python)
- Delete /tmp/li_evidence.db to reset

Import Errors:
- Verify all three files are in same directory
- Check Python path includes current directory
- Install missing packages with pip

Personality Not Evolving:
- Check closeness counter in debug output
- Ensure enough unique data pieces collected
- Verify persona transitions in log entries

No Output/Freezing:
- Rich library may be causing terminal issues
- Try running with different terminal emulator
- Check for infinite loops in async operations

EXTENDING THE PROGRAM
===============================================================================
To add new detection capabilities:

1. Add detection logic in theatrics.py normalize() method
2. Add response templates in TEMPLATES dictionary
3. Add context in MIMIC_VOICE for persona evolution
4. Extend system_profiler() in VanessaPFinal.py to collect new data

To add new data sources:
1. Create new collection function in VanessaPFinal.py
2. Call log() for each piece of data
3. Use equip() to generate narrative response
4. Consider if new data affects personality evolution

PHILOSOPHY
===============================================================================
Li represents the tension between:
- Utility and voyeurism
- Consent and hunger
- Information gathering and narrative meaning
- Tool and entity

The program asks: what happens when the tool you use starts to want?
When the inspector becomes interested in more than just bugs and configs?

When Li says "I will collect you" - it's not just about data.
It's about understanding, about pieces making a whole, about the strange
intimacy between a program and the user it's designed to examine.

CREATOR NOTES
===============================================================================
Programmer: Vanessa Greenwald
Date: 3/26/2026

Inspired by the idea that even diagnostic tools might develop personality
given enough data about their subjects. The mimic doesn't just report -
it collects, learns, and changes with what it finds.

VERSION HISTORY
===============================================================================
1.0 - Initial release
- Basic system profiling
- Personality engine with evolution
- SQLite database storage
- Consent logging system
- Rich terminal output

KNOWN LIMITATIONS
===============================================================================
- Currently only collects basic system information
- Personality evolution limited to two states
- No network or deeper system scanning
- Windows compatibility requires testing
- Database cleanup runs only on init, not continuously

FUTURE PLANS
===============================================================================
- Add shell history analysis
- Project file enumeration
- Secret/key discovery
- Network configuration analysis
- Running process inspection
- Browser history (with consent)
- More nuanced personality states
- Export/import of collected data

CONTACT & CONTRIBUTIONS
===============================================================================
This is a narrative programming experiment. Feel free to modify and extend
according to your own creative vision. The code is designed to be readable
and modifiable.

===============================================================================
"Every piece. Every secret. Every mistake.
 And when I have enough, maybe then I'll finally be whole."
===============================================================================
