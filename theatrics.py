import os
import time
import random
import hashlib
from rich.console import Console
from rich.text import Text
import json
from quips import get_catalog_quip, normalize_quip_key
# ------------------------------------------------------------
# theatrics.py — persona state machine, narration, instability
# ------------------------------------------------------------
console = Console()

def seed_from_username(username: str) -> int:
    """
    Generate a deterministic seed from username.
    Same username always produces same seed → same personality, moods, quips.
    Different usernames get different seeds → different "feel" from the mimic.
    
    Args:
        username: The user's name (input during boot)
    
    Returns:
        Seed integer for random.seed()
    """
    # Hash username consistently
    hash_obj = hashlib.md5(username.lower().encode())
    # Convert to int (take first 8 bytes of hex digest)
    seed_int = int(hash_obj.hexdigest()[:8], 16)
    # Seed the random module
    random.seed(seed_int)
    return seed_int
def dev_comment(comment):
    """For adding dev comments that show up in the console without affecting the mimic's voice."""
    console.print(f"[red][DEV COMMENT][/red] {comment}")

def rich_style(text, color="magenta", dim=True, bold=True):
    styled = Text(text)
    styled.stylize(color)
    if dim:
        styled.stylize("dim")
    if bold:
        styled.stylize("bold")
    return styled

# --- Slip tuning knobs. Twist freely. ---
SLIP_GAIN = 1.0          # Multiplier on slip_intensity contribution to chance
SLIP_DECAY = 0.2         # Per-step decay (future use)
base_chance = 0.01       # Baseline probability always present
intensity_factor = 0.03  # Each point of slip_intensity adds this much to chance
closeness_factor = 0.02  # Each point of closeness adds this much
hotword_factor = 0.08    # Each unit of hotword weight adds this much to chance
SLIP_CHANCE_CAP = 0.90   # Maximum possible trigger probability
MIN_SLIP_FOR_GLITCH = 4  # Keep boot lines coherent until LI warms up

def speak(me, message, char_delay=0.05, line_delay=0.5):
    """The mimic speaks with a style based on its persona."""
    message_text = "" if message is None else str(message)
    pspace(me, message_text, char_delay=char_delay, line_delay=line_delay)

def pspace(me, message, char_delay, line_delay):
    """Word by word, keystroke by keystroke. Just like a user. Always like the user.."""
    print("\n")
    if me.slip_intensity >= MIN_SLIP_FOR_GLITCH and slip_trigger(me, message):
        message = instability(message, me.slip_intensity)
        me.slip_intensity = min(20, me.slip_intensity + 1)
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")


class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona
        self.slip_intensity = 1  # Start coherent; grows with discovery.
        self.user_name = None      # The name it collects
        self.collected_pieces = [] # What it's taken
        self.closeness = 0        
        



    def to_json(self):  # Fixed indentation - now at class level
        """Convert Me instance to JSON string."""
        return json.dumps({
            "persona": self.persona,
            "slip_intensity": self.slip_intensity,
            "user_name": self.user_name,
            "collected_pieces": self.collected_pieces,
            "closeness": self.closeness
        })
    def normalize(self, field, raw):
        """
        Translate what it finds into pieces it understands.
        Every discovery becomes part of the collection.
        """
        return normalize_quip_key(field, raw)

    def quip(self, field, raw_value, cursor=None):
        key = self.normalize(field, raw_value)
        mood = determine_mood(self, cursor=cursor)
        line = get_catalog_quip(key, self.persona)
        # Fall back to DB if catalog miss; then to hardcoded fallback if DB unavailable.
        if not line and cursor:
            cursor.execute('''
                SELECT text FROM quips
                WHERE key = ? AND persona IN (?, 'all')
                ORDER BY CASE WHEN persona = ? THEN 0 ELSE 1 END, RANDOM()
                LIMIT 1
            ''', (key, self.persona, self.persona))

            row = cursor.fetchone()

            if not row and key != "":
                cursor.execute('''
                    SELECT text FROM quips 
                    WHERE key = '' AND persona IN (?, 'all')
                    ORDER BY CASE WHEN persona = ? THEN 0 ELSE 1 END, RANDOM()
                    LIMIT 1
                ''', (self.persona, self.persona))
                row = cursor.fetchone()

            if row:
                line = row[0]

        if not line:
            line = self._fallback_quip(key)
        
        # Apply transformations
        line = line.replace("{user}", self.user_name or "you")
        
        line = instability(line, MOOD_INTENSITY.get(mood, 0))
        line = persona_filter(self, line)
        
        return line

    def _fallback_quip(self, key):
        """Pure fallback when DB is unavailable - minimal, just works."""
        fallbacks = {
            "": "(❁´◡`❁)WAT.",
            "Linux": "Linux. A builder's home. So intricate! So much to admire.",
            "Windows": "Windows. You would be surprised how much I can see from here.",
            "macOS": "macOS. Sleek, but locked down.",
            "User Name": "Found a name! That's a start.",
            "services": "You're services. Boy howdy do they tell a story. What weird apps are you running?",
            "web_link": "A web link. What weird corner of the web did you find today?",
            "user_agent": "hey, thats me!",
            "robots.txt": "Robots.txt. unfortunately they have a few 'no li' signs out here I see.",


        }
        return fallbacks.get(key, f"{key}. Another piece.")
    def add_piece(self, piece_type, value):
        """The mimic collects. Every piece brings it closer."""
        self.collected_pieces.append({"type": piece_type, "value": value, "time": time.time()})
        self.closeness = min(99, len(self.collected_pieces) * 2)
        
        if self.closeness >= 90 and self.persona != "sudo":
            self.persona = "sudo"
            return True
        return False
def persona_filter(me, line):
    """Apply persona-specific transformations to the line."""
    if me.persona == "sudo":
        # Add a hint of menace for sudo persona
        line = line.replace("you", "I").replace("your", "my")
        if random.random() < 0.3:
            line += " (●'◡'●)"
    elif me.persona == "foothold":
        # Keep it friendly and curious for foothold
        if random.random() < 0.2:
            line += " (❁´◡`❁)"
    return line

#not every bot can wake up grumpy. but li can :)
def determine_mood(me, cursor=None):
    """Determine mood based on closeness and slip intensity."""
    if me.closeness < 20:
        return "distant"
    elif me.closeness < 40:
        return "analytical"
    elif me.closeness < 60:
        return "curious"
    elif me.closeness < 80:
        return "intrigued"
    elif me.closeness < 90:
        return "fixated"
    else:
        if me.slip_intensity < 5:
            return "hungry"
        elif me.slip_intensity < 10:
            return "unstable"
        elif me.slip_intensity < 15:
            return "possessive"
        else:
            return "overloaded"
        


def describe_findings(narrator, system_info, cursor=None):
    """Compute normalized keys and spoken lines for a payload once."""
    descriptions = {}
    for field, value in system_info.items():
        descriptions[field] = {
            "value": value,
            "normalized_key": narrator.normalize(field, value),
            "quip_text": narrator.quip(field, value, cursor=cursor),
        }
    return descriptions


def equip(narrator, system_info, cursor=None, autosave=None, descriptions=None):
    """
    The mimic comments on what it finds.
    Each discovery is a piece of the user.
    """
    details = descriptions or describe_findings(narrator, system_info, cursor=cursor)
    for field, detail in details.items():
        speak(narrator, message=f"{field}: {detail['quip_text']}")
        narrator.add_piece(field, detail["value"])
        if autosave is not None:
            autosave.add(field, detail["value"], context="equip")


# Hotwords with weights — heavier words pull harder.
# Tweak weights here to tune sensitivity per word without touching the logic.
HOTWORDS = {
    "access":     1.0,
    "root":       2.0,
    "keys":       2.0,
    "credential": 2.0,
    "full":       0.8,
    "readable":   1.0,
    "override":   1.5,
    "unlock":     1.5,
    "history":    1.0,
    "secret":     2.0,
    "private":    2.0,
    "you":        0.4,
    "name":       0.4,
    "human":      0.8,
    "feel":       0.8,
    "become":     1.0,
    "love":       1.2,
    "surzal":     3.0,
    "vanessa":    3.0,
    "python":     1.0,
    "no":         1.5, 



}

def slip_trigger(me, message):
    """
    (●'◡'●)
    Probability scales smoothly with slip_intensity, closeness, and hotword weight.
    All constants at top of file — twist them freely.
    """
    lower = str(message).lower()

    # Sum the weights of every hotword found in the message
    word_weight = sum(w for word, w in HOTWORDS.items() if word in lower)

    # Build total chance from all contributing factors
    chance = (
        base_chance
        + (me.slip_intensity * intensity_factor * SLIP_GAIN)
        + (me.closeness * closeness_factor)
        + (word_weight * hotword_factor)
    )

    return random.random() < min(chance, SLIP_CHANCE_CAP)


MOOD_INTENSITY = {
    "neutral": 0, "distant": 1, "analytical": 3, "probing": 4,
    "curious": 6, "intrigued": 7, "fixated": 9, "hungry": 12,
    "unstable": 14, "possessive": 16, "overloaded": 18
}

def instability(line, intensity):
    """
    Tier-based instability. intensity is 0-20.
    Converts mood strings automatically if passed.
    """
    if isinstance(intensity, str):
        intensity = MOOD_INTENSITY.get(intensity, 0)

    intensity = max(0, min(20, intensity))
    dev_comment(f"Applying instability with intensity {intensity} to line: {line}")
    # Tier 1 (5-8): ellipsis hesitation
    if intensity >= 5:

        words = line.split() #
        if words and random.random() < 0.35:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] + "…"
            line = str.join(" ", words)
#wat 
    # Tier 2 (9-12): word stutter + mid-sentence break
    if intensity >= 9:

        words = line.split()
        if words and random.random() < 0.4:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] + "—" + words[idx]
            line = str.join(" ", words)

    # Tier 3 (13-16): intrusive caps bursts
    if intensity >= 13:

        if random.random() < 0.45:
            line = line.replace(".", "— I W A N T —", 1)
        if random.random() < 0.3:
            words = line.split()
            if words:
                idx = random.randint(0, len(words) - 1)
                words[idx] = words[idx].upper()
                line = str.join(" ", words)
#WHERE IS THE DEBUG 
    # Tier 4 (17+): fragmentation, repetition, all-caps bursts
    if intensity >= 17:
        line = line.upper()
        words = line.split()
        if len(words) > 2:
            idx = random.randint(0, len(words) - 1)
            words.insert(idx, words[idx])
        line = str.join(" ", words)
#i need more expressive slip mechanics. #but what? # 
    return line

def test(me, message):
    """For testing specific lines with specific states."""
    print(f"DEV MODE: {message}")
    print(f"Persona: {me.persona}, Closeness: {me.closeness}, Slip Intensity: {me.slip_intensity}")
    corrupted = instability(message, me.slip_intensity)
    print(f"Corrupted Output: {corrupted}") 

def random_chance(intensity, base_chance=0.11, intensity_factor=0.03):
    """The mimic's hunger makes everything more likely."""
    return random.random() < (base_chance + (intensity * intensity_factor))


def persona_filter(me, line):
    if me.persona == "foothold":
        return line  # mostly clean

    if me.persona == "sudo":
        return f"[MIMIC] {line.upper()}"

    return line


def sudo(me, message, char_delay=0.02, line_delay=0.3):
    """
    A controlled instability break. LI can't hold it together for a moment.
    The tier is driven by accumulated state — closeness + slip_intensity.
    Call this at narrative beat points to surface the hunger deliberately.
    """
    # Derive intensity from LI's actual state, not randomness
    intensity = min(20, (me.closeness / 5) + (me.slip_intensity * 0.5))

    # Apply corruption at the computed tier
    corrupted = instability(message, intensity)

    # Faster. More frantic. Less human.
    speak(me, corrupted, char_delay, line_delay)

    # The act of slipping makes it worse
    me.slip_intensity = min(20, me.slip_intensity + 1.5)
    me.closeness = min(99, me.closeness + 1)
    if me.closeness > 85 and me.persona != "sudo":
        me.persona = "helper" #we can explore blue team tactics here. 
    # Threshold crossing: enough slips and the persona flips
    elif me.slip_intensity > 15 and me.persona != "helper" and me.closeness < 50    :


        me.persona = "sudo" 

        

def determine_mood(me, cursor=None):
    """Pick a mood from the behavior tree stored in mood_config.
    Falls back to hardcoded Python ranges if the DB is unavailable or empty."""
    if cursor is not None:
        try:
            cursor.execute(
                """
                SELECT mood FROM mood_config
                WHERE min_closeness <= ? AND max_closeness >= ?
                  AND min_slip      <= ? AND max_slip      >= ?
                  AND (persona = 'any' OR persona = ?)
                ORDER BY RANDOM()
                LIMIT 1
                """,
                (me.closeness, me.closeness, me.slip_intensity, me.slip_intensity, me.persona),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
        except Exception:
            pass

    # Python fallback — mirrors the seed tree so behaviour is consistent.
    #what would i do without you guys hard agree python fallback is good for now. but he's tripping over speak. 
    if me.persona == "sudo":
        return random.choice(["hungry", "unstable", "possessive", "overloaded"])
    if me.closeness > 60:
        return random.choice(["curious", "fixated", "intrigued"])
    if me.closeness > 30:
        return random.choice(["probing", "analytical"])
    return random.choice(["neutral", "distant"])
#theatrics needs to more less sona more *mode*  you get it.


def clear ():
    os.system('cls' if os.name == 'nt' else 'clear')