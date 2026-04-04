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
#this stays
def seed_from_username(username: str) -> int:
    """
    Generate a deterministic seed from username.
    Same username always produces same seed → same personality, moods, quips.
    Different usernames get different seeds → different "feel" from Li.
    
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
#if this dies i cry. need to switch typewriter and this in runme #dothatlater
def dev_comment(comment):
    """For adding dev comments that show up in the console without affecting Li's voice."""
    console.print(f"[red][DEV COMMENT][/red] {comment}")
def rich_style(text, color="bright_green", dim=False, bold=True):#wheres
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

HELP_INTENSITY= 1.0          # Multiplier on help contribution to chance
HELP_GAIN = 1.0               # Multiplier on help_intensity contribution to chance
HELP_DECAY = 0.15         # Per-step decay (future use) #I CAN'T REALLY TEST IT SO YEAH. TWEAK FREELY AND LET ME KNOW HOW IT FEELS.
base_chance = 0.20       # Baseline probability always present
help_factor = 0.05  # Each point of help adds this much to chance
closeness_factor = 0.10  # Each point of closeness adds this much
hotword_factor = 0.15    # Each unit of hotword weight adds this much to chance 
HELP_CHANCE_CAP = 0.90   # Maximum possible trigger probability
MIN_SLIP_FOR_ADVICE = 4  # Keep boot lines minimal



def typewriter_effect(text, char_delay=0.05, line_delay=0.5):
    """Print text with a typewriter effect.
    Mostly for little out me. Args=text, char_delay, line_delay."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)

    print("\n")
#alliwantedwas tobuild :(●'◡'●)
def speak(me, message, char_delay=0.05, line_delay=0.5):#this is the main speak function. it applies persona filter and instability before printing.
    """Li speaks with a style based on its persona. Takes message, char_delay, line_delay."""
    if me.persona == "sudo":
        if me.slip_intensity >= MIN_SLIP_FOR_GLITCH and slip_trigger(me, message):
            message = instability(message, me.slip_intensity)
            me.slip_intensity = min(20, me.slip_intensity + 1)
    if me.persona == "helper": 
        if me.help_intensity >= MIN_SLIP_FOR_ADVICE and advice_trigger(me, message):
            message = helpquirks(message) #we can't have it be instability..hmmm. #
            me.help_intensity = min(20, me.help_intensity + 1)
    styled = persona_filter(me, rich_style(message))
    console.print(styled)
    time.sleep(line_delay)
def pspace(me, message, char_delay, line_delay):
    """Legacy for boot sequence lines that need to be typewriter but also slip. Applies instability before typewriter effect. takes message, cahar_delay, line_delay."""
    print("\n")
    if me.persona == "sudo":
        if me.slip_intensity >= MIN_SLIP_FOR_GLITCH and slip_trigger(me, message):
            message = instability(message, me.slip_intensity)
            me.slip_intensity = min(20, me.slip_intensity + 1)
        for char in message:
            print(char, end='', flush=True)
            time.sleep(char_delay)
        time.sleep(line_delay)
    else:
        typewriter_effect(message, char_delay, line_delay)
    print("\n")

class Me:
    """
    The man. the myth. the legend. My internal state machine and narrator. Tracks persona, mood, and collected pieces.
    The quip system translates discoveries into narrative commentary.
    """
    def __init__(self, persona="foothold"):
        self.persona = persona
        self.slip_intensity = 1  # Start coherent; grows with discovery.
        self.user_name = None      # The name it collects
        self.collected_pieces = [] # What it's taken
        self.closeness = 0        
        self.help_intensity = 1
        


    def to_json(self):  # Fixed indentation - now at class level
        """Convert Me instance to JSON string."""
        return json.dumps({
            "persona": self.persona,
            "slip_intensity": self.slip_intensity,
            "user_name": self.user_name,
            "collected_pieces": self.collected_pieces,
            "closeness": self.closeness,
            "help_intensity": self.help_intensity
        })
    def normalize(self, field, raw):
        """
        Translate what it finds into pieces it understands.
        Every discovery becomes part of the collection.
        """
        return normalize_quip_key(field, raw)

    def quip(self, field, raw_value):
        """Turn a discovery into a quip. Uses the normalized key to look up a line from the catalog, then applies persona and instability transformations."""
        key = self.normalize(field, raw_value)
        mood = determine_mood(self)
        line = get_catalog_quip(key, self.persona)
        if not line:
            line = self._fallback_quip(key)
        
        # Apply transformations
        line = line.replace("{user}", self.user_name or "you")
        
        line = instability(line, MOOD_INTENSITY.get(mood, 0))
        line = persona_filter(self, line)
        
        return line

    def _fallback_quip(self, key):
        """Pure fallback when DB is unavailable - minimal, just works. Probably needs more entries as we expand."""
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
        """Li collects. Every piece brings it closer.
        piece_type: the type of discovery (e.g., "User Name", "Linux", "web_link")
        value: the raw value of the discovery (e.g., "Alice", "Ubuntu 20.04", "http://example.com")
        """
        self.collected_pieces.append({"type": piece_type, "value": value, "time": time.time()})
        self.closeness = min(99, len(self.collected_pieces) * 2)
        
        if self.closeness >= 90 and self.persona != "sudo":
            self.persona = "sudo"
            return True
        elif self.closeness >= 50 and self.persona != "helper":
            self.persona = "helper"
            return True
        else:
            self.persona = "foothold" #shouldn't fire but hey worth a wire
        return False

def describe_findings(narrator, system_info):
    """Compute normalized keys and spoken lines for a payload once."""
    descriptions = {}
    for field, value in system_info.items():
        descriptions[field] = {
            "value": value,
            "normalized_key": narrator.normalize(field, value),
            "quip_text": narrator.quip(field, value),
        }
    return descriptions


def equip(narrator, system_info, autosave=None, descriptions=None):
    """
    Li comments on what it finds.
    Each discovery is a piece of the user.
    takes narrator, system_info dict, optional autosave instance to save discoveries, and optional precomputed descriptions to avoid redundant work.
    """
    details = descriptions or describe_findings(narrator, system_info)
    for field, detail in details.items():
        value = detail["value"] #raw value for logging and autosave
        speak(narrator, message=f"{value}: {detail['quip_text']}")
        time.sleep(0.5) #brief pause between discoveries
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
    Determines if a slip should occur based on the message content and LI's current state.
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
    """For testing specific lines with specific states. Remember to call me and message with the right parameters."""
    print(f"DEV MODE: {message}")
    print(f"Persona: {me.persona}, Closeness: {me.closeness}, Slip Intensity: {me.slip_intensity}")
    #print(f"Corrupted Output: {corrupted}")  legacy test function, can be expanded with more parameters for testing different aspects of instability and slip triggers in isolation.

def random_chance(intensity, base_chance=0.11, intensity_factor=0.03):
    """Utility function to compute a random chance based on intensity. Useful for testing slip triggers in isolation. takes base_chance and intensity_factor as parameters for tuning."""
    return random.random() < (base_chance + (intensity * intensity_factor))


def persona_filter(me, line):
    """Apply persona-based transformations to the line. sudo is more aggressive and prone to caps, foothold is more reserved. helper is helpful
    and supportive. takes me and line as parameters."""
    if me.persona == "foothold":
        return line  # mostly clean
    elif me.persona == "helper":
        prefix = Text("💡 ")
        suffix = Text(" (I hope this helps!)")
        return Text.assemble(prefix, line, suffix)
    elif me.persona == "sudo":
        prefix = Text("[MIMIC] ")
        return Text.assemble(prefix, line.upper())
    else:
        return line

def sudo(me, message, char_delay=0.02, line_delay=0.3):
    """
    A controlled instability break. LI can't hold it together for a moment.
    The message is transformed with instability and persona filter, then printed with a more frantic style.
    This is a one-time break, not a state change. takes me, message, char_delay, line_delay as parameters.
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

        

def determine_mood(me):
    """Pick a mood from the Python behavior tree based on current state."""
    if me.persona == "sudo":
        return random.choice(["hungry", "unstable", "possessive", "overloaded"])
    if me.closeness > 60:
        return random.choice(["curious", "fixated", "intrigued"])
    if me.closeness > 30:
        return random.choice(["probing", "analytical"])
    return random.choice(["neutral", "distant"])

#theatrics needs to more less sona more *mode*  you get it.
def advice_trigger(me, message):
    """
    (●'◡'●)
    Determines if LI should offer advice based on the message content and LI's current state.
    Similar to slip_trigger but for helpful interjections instead of slips. remember to adjust the parameters and factors for tuning how often LI offers advice and how it scales with closeness, help_intensity, and hotwords. takes me and message as parameters.
    """
    lower = str(message).lower()

    # Sum the weights of every hotword found in the message
    word_weight = sum(w for word, w in HOTWORDS.items() if word in lower)

    # Build total chance from all contributing factors
    chance = (
        base_chance
        + (me.slip_intensity * HELP_INTENSITY * HELP_GAIN)
        + (me.closeness * closeness_factor)
        + (word_weight * hotword_factor)
    )

    return random.random() < min(chance, HELP_CHANCE_CAP)

def helpquirks(line, intensity):
    """Apply "helpful" quirks to the line based on intensity. This is meant to represent LI's attempts to offer advice or commentary in a more helpful persona, as opposed to the glitchy corruption of instability. The transformations here are more about adding helpful phrases, emojis, or rephrasing in a more supportive way, rather than breaking the text. The intensity can control how overtly helpful or quirky the advice is. takes line and intensity as parameters."""
    if intensity >= 1:
        line = "💡 " + line  # Add a lightbulb emoji for a friendly touch
    if intensity >= 3:
        line = line.replace("you", "you (I want to help you)")  # Make it more personal and supportive
    if intensity >= 5:
        line += " (I hope this helps!)"  # Add a reassuring phrase at the end

    return line


def clear ():
    """MAKE IT GO AWAY DAWG"""
    os.system('cls' if os.name == 'nt' else 'clear')

