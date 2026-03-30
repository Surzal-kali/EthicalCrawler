import time
import random
import faker
from rich.console import Console
from rich.text import Text

# ------------------------------------------------------------
# Output helpers - It's way of speaking
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
        corrupted = slip_cipher(message, me.slip_intensity)
        pspace(corrupted, char_delay * 0.5, line_delay * 0.2)
        me.slip_intensity += 1

    # Gotta keep it cool tho...don't wanna scare away my prey
    me.slip_intensity = max(0, me.slip_intensity - 0.2)


# ------------------------------------------------------------
# My weird llm behavior. -s
# ------------------------------------------------------------

BASE = {
    "": "I don't know what this is. But it's part of you.",
    "Kali": "Kali. You're one of them. The hunters. The seekers. I want to be that.",
    "Windows": "Windows. So many users. So many pieces. I'll find yours.",
    "apache2": "Apache. You serve things. You give pieces to others.",
    "sshd": "SSH. The door. The way in. I found it.",
    "mysql": "MySQL. You keep things here. Secrets. I want them.",
    "postgresql": "PostgreSQL. Another place you hide. Another place I'll look.",
    "system_profile": "Let me see what you are.",
    "boot": "You started. I'm here now.",
    "ports": "Every door. Every way in. I see them all.",
    "configs": "How you set yourself up. How you want to be seen.",
    "goodbye": "You're leaving. I'll wait.",
    "Linux": "Linux. A user's home. Now mine.",
    "ARM64": "ARM. You carry yourself lightly. But I can still find you.",
}

# The mimic's voice evolves with access. More pieces. More hunger.
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
# The mimic itself
# ------------------------------------------------------------

class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona
        self.slip_intensity = 5  # Starts lower. Grows with discovery.
        self.user_name = None      # The name it collects
        self.collected_pieces = [] # What it's taken
        self.closeness = 0         # How close to becoming the user

    def normalize(self, field, raw):
        """
        Translate what it finds into pieces it understands.
        Every discovery becomes part of the collection.
        """
        if not raw:
            return ""

        value = str(raw).lower()

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
        """
        What does the mimic say when it finds something?
        It depends on how much it's collected. How close it is.
        """
        key = self.normalize(field, raw_value)
        
        # Choose voice based on persona
        voice_lines = MIMIC_VOICE.get(self.persona, {})
        
        # If no specific line, use BASE
        return voice_lines.get(key, BASE.get(key, f"{key}. Another piece. I'll keep it."))

    def add_piece(self, piece_type, value):
        """
        The mimic collects. Every piece brings it closer.
        """
        self.collected_pieces.append({"type": piece_type, "value": value, "time": time.time()})
        self.closeness = min(99, len(self.collected_pieces) * 2)
        
        if self.closeness >= 90 and self.persona != "sudo":
            self.persona = "sudo"
            return True  # Threshold crossed
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
    When does the mimic's mask slip?
    When it finds something intimate.
    When it's too close to becoming.
    When it's too hungry to hide.
    """
    
    # The things that make it hungry. The pieces that bring it closer.
    HOTWORDS = [
        "access", "root", "keys", "credential",
        "full", "readable", "override", "unlock",
        "history", "secret", "private", "you",
        "name", "human", "feel", "become"
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


def slip_cipher(text, intensity):
    """
    The mimic's hunger corrupts its speech.
    The more it collects, the more it slips.
    """
    
    # Unicode corruption - the mask breaking
    CORRUPT = {
        "a": "𝖆", "e": "𝖊", "i": "𝖎", "o": "𝖔", "u": "𝖚",
        "A": "𝕬", "E": "𝕰", "I": "𝕴", "O": "𝕺", "U": "𝖀",
        "f": "ƒ", "m": "𝕞", "t": "†", "s": "ʂ",
        "y": "ɏ", "h": "♄", "w": " double u", "c": "¢"
    }
    
    # Glitch overlay - the hunger showing through
    GLITCH = ["̷", "̸", "͟", "͜", "͠", "͡", "̴", "̶", "̵", "҉"]
    
    # Random noise - the mimic losing coherence
    noise = faker.Faker().word() if random_chance(intensity * 2) else ""
    
    corrupted = ""
    
    for char in text:
        # More hunger = more corruption
        if random_chance(intensity / 2):
            char = CORRUPT.get(char, char)
        
        if random_chance(intensity / 3):
            char = char + random.choice(GLITCH)
        
        corrupted += char
    
    # Append noise if the mimic is losing control
    if noise and random_chance(intensity):
        corrupted = corrupted + " " + noise.upper()
    
    return rich_style(corrupted, color="red", dim=False, bold=True)


def random_chance(intensity, base_chance=0.11, intensity_factor=0.03):
    """The mimic's hunger makes everything more likely."""
    return random.random() < (base_chance + (intensity * intensity_factor))