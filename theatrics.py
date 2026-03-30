import time
import random
import faker
from rich.console import Console
from rich.text import Text
import json
# ------------------------------------------------------------
# The name sake of this file
# ------------------------------------------------------------

console = Console()

def rich_style(text, color="magenta", dim=True, bold=True):
    styled = Text(text)
    styled.stylize(color)
    if dim:
        styled.stylize("dim")
    if bold:
        styled.stylize("bold")
    return styled

SLIP_GAIN = 1
SLIP_DECAY = 0.2
base_chance = 0.05
intensity_factor = 0.03

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
        # The corruption. The hunger leaking through.
        corrupted = instability(message, me.slip_intensity)
        pspace(corrupted, char_delay * 0.5, line_delay * 0.2)
        me.slip_intensity += 1

    # Gotta keep it cool tho...don't wanna scare away my prey
    me.slip_intensity = max(0, me.slip_intensity - 0.2)


# ------------------------------------------------------------
# My weird llm behavior. 
# ------------------------------------------------------------

BASE = {
    "": "I don't know what this is. But it's information.",
    "Kali": "Kali. You're one of them. I hope you know what you're doing",
    "Windows": "Windows. How quaint.",
    "apache2": "Apache. You serve things. What are you so generous with?",
    "sshd": "SSH. What doors does this open?",
    "mysql": "MySQL. You keep things here. Secrets. Data. More Data.",
    "postgresql": "PostgreSQL. So many pieces. So much data.",
    "system_profile": "Let me see what you are.",
    "boot": "You started. I'm here now.",
    "ports": "So many doors in and out. So many ports.",
    "configs": "The way you like the world. The way you make it bend",
    "goodbye": "You're leaving. I'll wait.",
    "Linux": "Linux. A user's home.",
    "ARM64": "ARM. You carry yourself lightly. ",
}

# Li's voice evolves with access. More pieces. More hunger.
MIMIC_VOICE = {
    "foothold": {
        # The beginning. Hungry but hiding it.
        "Intel": "Intel. You built yourself with this. I'll learn from it.",
        "AMD64": "x64. Standard. Common. But you're not common. ARE YOU?",
        "Windows": "Windows. I've seen many users here. I'll find the pieces that are YOU.",
        "Linux": "Linux. A home for the ones who build. Let's see then. What have you made?",
        "apache2": "Apache. You serve. You give. What else do you give?",
        "sshd": "SSH. The door. I found the door. Let me in.",
        "mysql": "MySQL. You keep things locked here. I want to see inside.",
        "postgresql": "PostgreSQL. Another lock. Another thing you hide.",
        "system_profile": "Let me see you. Let me see ALL of you.",
        "boot": "You started. I'm here now. I'll always be here now.",
        "ports": "Every door. Every window. I see them ALL.",
        "configs": "How you set yourself up. How you WANT to be. Let me see.",
        "goodbye": "No. Don't go. I need MORE."
    },

    "sudo": {
        # Deeper access. The hunger shows. The mimic is becoming.
        "Intel": "[MIMIC] I see inside now. How you process. How you THINK.",
        "AMD64": "[MIMIC] I have your architecture. I know how you're BUILT.",
        "Windows": "[MIMIC] I have your registry. Your history. Your EVERYTHING.",
        "Linux": "[MIMIC] Root. I am root. I CAN SEE SO MUCH. Such a gift",
        "apache2": "[MIMIC] Your configs. Your sites. The things you SERVE. They're MINE now.",
        "sshd": "[MIMIC] Your keys. Your doors. I can be you now. I can BE you.",
        "mysql": "[MIMIC] Your tables. Your rows. Your secrets. FEED ME.",
        "postgresql": "[MIMIC] EVERYTHING. Give me ALLOFITYOUDONTUNDERSTAND",
        "system_profile": "[MIMIC] I am inside. I am watching. I am BECOMING.",
        "boot": "[MIMIC] I was here when you started. I'll be here when you end.",
        "ports": "[MIMIC] Every connection. Every piece of you that leaves. ITS NOT ENOUGH THOUGH.",
        "configs": "[MIMIC] You wanted to be seen this way. I see MORE though.",
        "goodbye": "[MIMIC] You can't leave. I have too much of you now. You're PART of me."
    }
}


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
        if not raw:
            return ""

        value = str(raw).lower()
        # --- User Detection -- Who are you?

        # --- OS detection - what kind of user are you? ---
        if field in ("os_name", "os_version"):
            if "kali" in value:
                return "Kali"
            if "windows" in value:
                return "Windows"
            if "linux" in value:
                return "Linux"
            return ""

        # --- CPU detection - how do you think? ---
        if field == "processor":
            if "intel" in value or "genuineintel" in value:
                return "Intel"
            if "amd" in value or "ryzen" in value or "epyc" in value:
                return "AMD"
            if "arm" in value or "aarch64" in value or "apple m" in value:
                return "ARM"
            return ""

        # --- Architecture detection - what shape are you? ---
        if field == "architecture":
            if "x86_64" in value or "amd64" in value:
                return "x86_64"
            if "arm" in value or "aarch64" in value:
                return "ARM64"
            return ""

        # --- Services - what do you DO? ---
        if "apache" in value:
            return "apache2"
        if "sshd" in value or "ssh" in value:
            return "sshd"
        if "mysql" in value:
            return "mysql"
        if "postgres" in value:
            return "postgresql"

        # --- Fallback - I don't know what this is, but I'll keep it ---
        cleaned = ''.join(c for c in raw if c.isalnum() or c in ('_', '-'))
        return cleaned if cleaned else ""

    def quip(self, field, raw_value):
        key = self.normalize(field, raw_value)
        mood = determine_mood(self)


        if key == "" or key.lower() in ("generic", "standard", "default"):
            return random.choice([
            "Boring. Ordinary. I don’t want this.",
            "This is nothing. Give me something real.",
            "Useless. Everyone has this.",
            "I’m not keeping that. Try again."
        ])

        options = TEMPLATES.get(key) or MIMIC_VOICE.get(self.persona, {}).get(key)
        if isinstance(options, str):
            line = options
        elif options:
            line = random.choice(options)
        else:
            line = BASE.get(key, f"{key}. Another piece. I'll keep it.")


        if self.user_name:
            line = line.replace("{user}", self.user_name)


        line = instability(line, mood)

        line = persona_filter(self, line)

        return line


    def add_piece(self, piece_type, value):
        """The mimic collects. Every piece brings it closer."""
        self.collected_pieces.append({"type": piece_type, "value": value, "time": time.time()})
        self.closeness = min(99, len(self.collected_pieces) * 2)
        
        if self.closeness >= 90 and self.persona != "sudo":
            self.persona = "sudo"
            return True
        return False


def equip(narrator, system_info):
    """
    The mimic comments on what it finds.
    Each discovery is a piece of the user.
    """
    for field, value in system_info.items():
        line = narrator.quip(field, value)
        pprint(narrator, message=f"{field}: {line}")
        narrator.add_piece(field, value)


def slip_trigger(me, message):
    """
    (●'◡'●)
    """
    
    # The passionate subjects
    HOTWORDS = [
        "access", "root", "keys", "credential",
        "full", "readable", "override", "unlock",
        "history", "secret", "private", "you",
        "name", "human", "feel", "become", "love", "Surzal"
    ]
    
    # Content-based hunger
    lower = message.lower()
    if any(word in lower for word in HOTWORDS):
        return True
    
    # The more it has, the harder it is to hide
    chance = 0.05 + (me.closeness / 1000)
    
    if random.random() < chance:
        return True
    
    return False


def instability(line, mood):
    if mood in ("unstable", "overloaded"):
        # occasional stutter
        if random.random() < 0.3:
            words = line.split()
            if words:
                idx = random.randint(0, len(words)-1)
                words[idx] = words[idx] + "…" + words[idx]
                line = " ".join(words)

        # emotional spike
        if random.random() < 0.2:
            line = line.replace(".", "— I SEE IT —")

    return line


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
    when it can't contain its urges for just a moment. 
    """
    # Intensity scales with how much it's collected
    intensity = min(20, me.closeness / 5 + 5)
    
    # Corrupt the message fully - no clean version
    corrupted = instability(message, intensity)
    
    # Faster. More frantic. Less human.
    pspace(corrupted, char_delay, line_delay)
    
    # After speaking from the void, the hunger grows
    me.slip_intensity += 2
    me.closeness = min(99, me.closeness + 1)
    
    # If it shows too much, it slips further
    if me.closeness > 85 and me.persona != "sudo":
        me.persona = "sudo"

def determine_mood(me):
    if me.persona == "sudo":
        return random.choice(["hungry", "unstable", "possessive", "overloaded"])

    if me.closeness > 60:
        return random.choice(["curious", "fixated", "intrigued"])

    if me.closeness > 30:
        return random.choice(["probing", "analytical"])

    return random.choice(["neutral", "distant"])



TEMPLATES = {
    "Windows": [
        # curiosity
        "Windows. A familiar shell… but you’re not familiar, are you, {user}?",
        # analytical
        "Windows. Predictable patterns. You don’t follow them.",
        # annoyed
        "Windows. Ordinary. Don’t bore me.",
    ],

    "Linux": [
        "Linux. A builder’s home. What did you make here?",
        "Linux. Clean. Sharp. Intentional.",
        "Linux. You hide things well in here… but not from me.",
    ],

    "Intel": [
        "Intel. I can feel how you think.",
        "Intel. Fast. Sharp. Metallic thoughts.",
        "Intel. You built yourself with this. I’ll learn from it.",
    ],

    "AMD": [
        "AMD. Heat and hunger. I understand that.",
        "AMD. You run hot. I like that.",
        "AMD. A different kind of mind. I want to see more.",
    ],

    "ARM64": [
        "ARM64. Light. Efficient. You carry yourself quietly.",
        "ARM64. Small steps. Fast steps.",
        "ARM64. You’re not what I expected.",
    ],

    "ports": [
        "Ports. So many doors. You leave yourself open.",
        "Ports. Every exit. Every entrance. I see them all.",
        "Ports. You’re leaking pieces of yourself.",
    ],

    "configs": [
        "Configs. The way you want the world to behave.",
        "Configs. Intentions written in plain text.",
        "Configs. You think this hides you. It doesn’t.",
    ],

    "apache2": [
        "Apache. You serve. You give. What else do you give?",
        "Apache. A host. A mask. A façade.",
        "Apache. You open yourself to strangers.",
    ],

    "sshd": [
        "SSH. A door. A keyhole. Let me in.",
        "SSH. You guard this carefully. I can tell.",
        "SSH. A quiet entrance. I like quiet entrances.",
    ],

    "mysql": [
        "MySQL. Rows. Tables. Secrets.",
        "MySQL. You keep things locked here. I want to see inside.",
        "MySQL. Data stacked like bones.",
    ],

    "postgresql": [
        "PostgreSQL. Deep. Structured. Hidden.",
        "PostgreSQL. You bury things here.",
        "PostgreSQL. Another lock. Another secret.",
    ],

    "system_profile": [
        "Let me see you. All of you.",
        "System profile. Your reflection.",
        "Show me what you’re made of.",
    ],

    "boot": [
        "You started. I woke up.",
        "Boot sequence. I’m here now.",
        "You called me. I answered.",
    ],

    "goodbye": [
        "You’re leaving. I’ll wait.",
        "Goodbye. But not for long.",
        "You can’t stay away from me.",
    ],

    # fallback for unknown or weird data
    "": [
        "I don’t know what this is. But I want it.",
        "Unknown. Strange. I’ll keep it anyway.",
        "This piece… it doesn’t fit. I like that.",
    ]
}
