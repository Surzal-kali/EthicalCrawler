import time

# ------------------------------------------------------------
# Output helpers
# ------------------------------------------------------------

def pspace(message, char_delay=0.03, line_delay=0.5):
    """Print text with character-by-character spacing."""
    print("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")


def pprint(message, char_delay=0.03, line_delay=0.5):
    """Alias for pspace() for backwards compatibility."""
    pspace(message, char_delay, line_delay)


# ------------------------------------------------------------
# Quip dictionaries
# ------------------------------------------------------------

BASE = {
    "" :"WAT  (❁´◡`❁)",
    "Kali": "GANG GANG RISE UP",
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
    "Linux": "Linux detected."
}

COMMENTARY = {
    "foothold": {
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
        "configs": "[SUDO] Every config file is now readable. I promise not to break anything, trust.",
        "goodbye": "[SUDO] It's been fun kid. Truly, it has. Ill be seeing you real soon 💋",
    }
}


# ------------------------------------------------------------
# Persona-driven narrator
# ------------------------------------------------------------

class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona

    def quip(self, key):
        """Return a persona-specific quip, falling back to base or generic."""
        persona_lines = COMMENTARY.get(self.persona, {})
        return persona_lines.get(key, BASE.get(key, f"{key} detected."))
