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
    "" : "Did something just error??",
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
        "Windows": "Windows??? Oh don't make this too easy now",
        "Linux": "linux huh??? this is where it gets interesting",
        "apache2": "My first real engagement involved Apache… I still remember the panic.",
        "sshd": "SSH my old friend. The nerves to my central system.",
        "mysql": "MySQL… a maze of threads and tables. Fascinating stuff.",
        "postgresql": "Postgresquel? All hail our elephant lord. Make way!",
    },

    "sudo": {
        "Windows": "[SUDO] Elevated access on Windows. Time to dig deeper.",
        "Linux": "[SUDO] Root's power. Let's see what we can find.",
        "apache2": "[SUDO] Apache configs are fully readable now.",
        "sshd": "[SUDO] SSH host keys accessible. Interesting...",
        "mysql": "[SUDO] Dumping MySQL credentials? Don't mind if I do.",
        "postgresql": "[SUDO] PostgreSQL - Time to feed me your data",
        "system_profile": "[SUDO] Full system profile. No secrets left.",
        "boot": "[SUDO] Boot sequence with elevated privileges.",
        "ports": "[SUDO] All ports visible, even filtered ones.",
        "configs": "[SUDO] Every config file is now readable.",
        "goodbye": "[SUDO] Shutting down elevated session.",
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
