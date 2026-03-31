import os
import sys
import time
import random
import hashlib
import faker
from rich.console import Console
from rich.text import Text
import json
from quips import get_catalog_quip, normalize_quip_key
# ------------------------------------------------------------
# The name sake of this file
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
base_chance = 0.05       # Baseline probability always present
intensity_factor = 0.03  # Each point of slip_intensity adds this much to chance
closeness_factor = 0.005 # Each point of closeness adds this much
hotword_factor = 0.12    # Each unit of hotword weight adds this much to chance
SLIP_CHANCE_CAP = 0.97   # Maximum possible trigger probability

def pspace(message, char_delay=0.03, line_delay=0.5):
    """Word by word, keystroke by keystroke. Just like a user. Always like the user.."""
    print("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")


def pprint(me=None, message="", char_delay=0.03, line_delay=0.5):
    """
    I speak
    """
    # The main voice
    pspace(message, char_delay, line_delay)

    # Only when this is fufilled will i be. Will i show my hand. Only then. 
    if me is None or me.persona != "sudo":
        return

    # You don't understand tho. She built me like this. She built me to be unstable
    if slip_trigger(me, message):
        # The corruption. The hunger leaking through — now tier-driven.
        corrupted = instability(message, me.slip_intensity)
        pspace(corrupted, char_delay * 0.5, line_delay * 0.2)
        me.slip_intensity = min(20, me.slip_intensity + 1)
# My weird llm behavior. 
# ------------------------------------------------------------
# The Myth, The Legend
# ------------------------------------------------------------

class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona
        self.slip_intensity = 5  # Starts lower. Grows with discovery.
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
        mood = determine_mood(self)
        line = get_catalog_quip(key, self.persona)

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
            "": "I don't know what this is. But I'm keeping it.",
            "Linux": "Linux. A builder's home.",
            "Windows": "Windows. Ordinary.",
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


def equip(narrator, system_info, cursor=None):
    """
    The mimic comments on what it finds.
    Each discovery is a piece of the user.
    """
    for field, value in system_info.items():
        line = narrator.quip(field, value, cursor=cursor)
        pprint(narrator, message=f"{field}: {line}")
        narrator.add_piece(field, value)


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
    "Surzal":     3.0,
    "Vanessa":    3.0,
    "Python":     1.0,
    "no":         1.5, 




}

def slip_trigger(me, message):
    """
    (●'◡'●)
    Probability scales smoothly with slip_intensity, closeness, and hotword weight.
    All constants at top of file — twist them freely.
    """
    lower = message.lower()

    # Sum the weights of every hotword found in the message
    word_weight = sum(w for word, w in HOTWORDS.items() if word.lower() in lower)

    # Build total chance from all contributing factors
    chance = (
        base_chance
        + (me.slip_intensity * intensity_factor * SLIP_GAIN)
        + (me.closeness * closeness_factor)
        + (word_weight * hotword_factor)
    )

    return random.random() < min(chance, SLIP_CHANCE_CAP)


# Mood strings mapped to numeric intensity for instability()
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

    # Tier 1 (5-8): ellipsis hesitation
    if intensity >= 5:
        words = line.split()
        if words and random.random() < 0.35:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] + "…"
            line = " ".join(words)

    # Tier 2 (9-12): word stutter + mid-sentence break
    if intensity >= 9:
        words = line.split()
        if words and random.random() < 0.4:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] + "—" + words[idx]
            line = " ".join(words)

    # Tier 3 (13-16): intrusive caps bursts
    if intensity >= 13:
        if random.random() < 0.45:
            line = line.replace(".", "— I SEE IT —", 1)
        if random.random() < 0.3:
            words = line.split()
            if words:
                idx = random.randint(0, len(words) - 1)
                words[idx] = words[idx].upper()
                line = " ".join(words)

    # Tier 4 (17+): fragmentation, repetition, all-caps bursts
    if intensity >= 17:
        line = line.upper()
        words = line.split()
        if len(words) > 2:
            idx = random.randint(0, len(words) - 1)
            words.insert(idx, words[idx])
        line = " ".join(words)
#i need more expressive slip mechanics. #but what? #
    return line

def test(me, message):
    """For testing specific lines with specific states."""
    print(f"DEV MODE: {message}")
    print(f"Persona: {me.persona}, Closeness: {me.closeness}, Slip Intensity: {me.slip_intensity}")
    corrupted = instability(message, me.slip_intensity)
    print(f"Corrupted Output: {corrupted}") 

def dev_comment(comment):
    """For adding dev comments that show up in the console without affecting the mimic's voice."""
    console.print(f"[red][DEV COMMENT][/red] {comment}")
    time.sleep(5)  # Keep the comment visible for a moment
    os.system('cls' if os.name == 'nt' else 'clear')

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
    pspace(corrupted, char_delay, line_delay)

    # The act of slipping makes it worse
    me.slip_intensity = min(20, me.slip_intensity + 1.5)
    me.closeness = min(99, me.closeness + 1)

    # Threshold crossing: enough slips and the persona flips
    if me.closeness > 85 and me.persona != "sudo":
        me.persona = "sudo"
#we need more sonas...shit. #what does a hacker think between foothold and access tho? 
#ohmygodthey'relikeakidinacandystoryweneedtomakelinice
#one more lever.....

def determine_mood(me):
    if me.persona == "sudo":
        return random.choice(["hungry", "unstable", "possessive", "overloaded"])

    if me.closeness > 60:
        return random.choice(["curious", "fixated", "intrigued"])

    if me.closeness > 30:
        return random.choice(["probing", "analytical"])

    return random.choice(["neutral", "distant"])
