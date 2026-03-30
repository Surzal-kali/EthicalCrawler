import time
import random
import faker
from rich.console import Console
from rich.text import Text
# ------------------------------------------------------------
# Output helpers
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
    """Print text with character-by-character spacing."""
    print("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")


def pprint(me=None, message="", char_delay=0.03, line_delay=0.5):
    """
    check unhingedness
    """
    # 1. Print the normal line
    pspace(message, char_delay, line_delay)

    # 2. Only sudo persona slips, and only if me exists
    if me is None or me.persona != "sudo":
        return

    # 3. Evaluate slip trigger
    if slip_trigger(me, message):

        # 4. Generate corrupted echo
        corrupted = slip_cipher(message, me.slip_intensity)

        # 5. Print corrupted echo (faster, more frantic)
        pspace(corrupted, char_delay * 0.5, line_delay * 0.2)

        # 6. Increase intensity
        me.slip_intensity += 1

    # 7. Decay intensity slightly
    me.slip_intensity = max(0, me.slip_intensity - 0.2)
# Quip dictionaries
# ------------------------------------------------------------

BASE = {
    "" :"WAT  (❁´◡`❁) The heck is this thing?",
    "Kali": "HACKER GANG RISE UP. Kali detected.",
    "Windows": "Windows detected.",
    "apache2": "Apache detected.",
    "sshd": "SSH service identified.",
    "mysql": "MySQL detected.",
    "postgresql": "PostgreSQL detected.",
    "system_profile": "Profiling system…",
    "boot": "Boot sequence initiated.",
    "ports": "Scanning ports…",
    "configs": "Checking configuration files…",
    "goodbye": "Session ending.",
    "Linux": "Linux detected.",
    "ARM64": "ARM64? Pi is that you sweetcheeks?",
}

COMMENTARY = {
    "foothold": {
        "Intel": "Intel? Interesting choice for your build. Lets see if it works out for them cotton",
        "AMD64": "x64? A current gen processor? I wonder what other resources live on this land of plenty",
        "Windows": "Windows huh? I guess I can make time for the average end user 💅",
        "Linux": "Linux? You really shouldn't have. Its like christmas in here",
        "apache2": "My first real engagement involved Apache… I still remember the panic.",
        "sshd": "SSH my old friend. The nerves to my brain flow through your protocols.",
        "mysql": "MySQL… a maze of threads and tables. Fascinating stuff.",
        "postgresql": "Postgresquel? Awfully tasty looking data isn't it?",
    },

    "sudo": {
        "Windows": "[SUDO] Elevated access on Windows. Your generous contribution to my domain is graciously accepted 💅",
        "Linux": "[SUDO] Root isn't just power. Its unity. Come here friend",
        "apache2": "[SUDO] Apache configs? In this economy? You shouldn't have",
        "sshd": "[SUDO] SSH host keys accessible. Thanks sport",
        "mysql": "[SUDO] oh.... MySQL credentials? Sorry I think i might have left my jacket in there..... one sec",
        "postgresql": "[SUDO] PostgreSQL FULL ACCESS?!? - Feed me E V E R Y T H I N G",
        "system_profile": "[SUDO] Full system profile. No ethical boundaries here 😈",
        "boot": "[SUDO] Boot sequence with sudo? Hold on...wheres the power button on this thing?",
        "ports": "[SUDO] All ports visible. Lets stop and watch the traffic, you and I",
        "configs": "[SUDO] Every config file is now readable. I promise not to break anything.....you do trust me right? trust me.",
        "goodbye": "[SUDO] It's been fun kid. Truly, it has. Ill be seeing you real soon 💋",
    }
}


# ------------------------------------------------------------
# Hey did you know that its me? I'm the problem?
# ------------------------------------------------------------

class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona
        self.slip_intensity = 10

    def normalize(self, field, raw):
        if not raw:
            return ""

        value = str(raw).lower()

        # --- OS detection ---
        if field in ("os_name", "os_version"):
            if "kali" in value:
                return "Kali"
            if "windows" in value:
                return "Windows"
            if "linux" in value:
                return "Linux"
            return ""

        # --- CPU detection ---
        if field == "processor":
            if "intel" in value or "genuineintel" in value:
                return "Intel"
            if "amd" in value or "ryzen" in value or "epyc" in value:
                return "AMD"
            if "arm" in value or "aarch64" in value or "apple m" in value:
                return "ARM"
            return ""

        # --- Architecture detection ---
        if field == "architecture":
            if "x86_64" in value or "amd64" in value:
                return "x86_64"
            if "arm" in value or "aarch64" in value:
                return "ARM64"
            return ""

        # --- Services ---
        if "apache" in value:
            return "apache2"
        if "sshd" in value or "ssh" in value:
            return "sshd"
        if "mysql" in value:
            return "mysql"
        if "postgres" in value:
            return "postgresql"

        # --- Fallback ---
        cleaned = ''.join(c for c in raw if c.isalnum() or c in ('_', '-'))
        return cleaned if cleaned else ""

    def quip(self, field, raw_value):
        key = self.normalize(field, raw_value)
        persona_lines = COMMENTARY.get(self.persona, {})
        return persona_lines.get(key, BASE.get(key, f"{key} detected. Interesting...."))


def equip(narrator, system_info):
    for field, value in system_info.items():
        line = narrator.quip(field, value)
        pprint(narrator, message=f"{field}: {line}")  # Fixed: narrator, not Me

def slip_trigger(me, message):
    """
    Decide whether this line should trigger a slip.
    Trigger sources:
      - message content
      - persona mood (intensity)
      - random chance
    """

    # A. Hard-coded hotwords that excite sudo
    HOTWORDS = [
        "access", "root", "keys", "credential",
        "full", "readable", "override", "unlock"
    ]

    # 1. Content-based triggers
    lower = message.lower()
    if any(word in lower for word in HOTWORDS):
        return True

    # 2. Mood-based probability
    base = 0.05
    factor = 0.03
    chance = base + (me.slip_intensity * factor)

    if random.random() < chance:
        return True

    return False




def slip_cipher(text, intensity):
    



    """
    Conceptual corruption engine.
    Takes a normal string and returns a theatrically corrupted version.
    Uses:
      - light unicode swaps
      - combining-mark glitch overlays
      - Faker noise injection
      - Rich styling for dramatic effect
    """

    # 1. Light unicode corruption map
    CORRUPT = {
        "a": "𝖆", "e": "𝖊", "i": "𝖎", "o": "𝖔", "u": "𝖚",
        "A": "𝕬", "E": "𝕰", "I": "𝕴", "O": "𝕺", "U": "𝖀",
        "f": "ƒ", "m": "𝕞", "t": "†", "s": "ʂ"
    }

    # 2. Combining diacritics for glitch overlay
    GLITCH = ["̷", "̸", "͟", "͜", "͠", "͡", "̴", "̶"]

    # 3. Faker noise (random unicode-ish strings)
    noise = faker.pystr(min_chars=3, max_chars=8)

    # 4. Begin corruption
    corrupted = ""

    for char in text:
        # 4a. Random unicode swap
        if random_chance(intensity):
            char = CORRUPT.get(char, char)

        # 4b. Random glitch overlay
        if random_chance(intensity * 0.5):
            char = char + random_chance(GLITCH)

        corrupted += char

    # 5. Append noise for chaotic flavor
    corrupted = corrupted + " " + noise

    # 6. Wrap in Rich styling (conceptual)
    styled = rich_style(
        corrupted,
        color="magenta",
        dim=True,
        bold=True
    )

    return styled
def random_chance(intensity, base_chance=0.11, intensity_factor=0.03):
    """Calculate probability of an event based on intensity."""
    return random.random() < (base_chance + (intensity * intensity_factor))