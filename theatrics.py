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
        "configs": "[SUDO] Every config file is now readable. I promise not to break anything, trust.",
        "goodbye": "[SUDO] It's been fun kid. Truly, it has. Ill be seeing you real soon 💋",
    }
}


# ------------------------------------------------------------
# Hey did you know that its me? I'm the problem?
# ------------------------------------------------------------

class Me:
    def __init__(self, persona="foothold"):
        self.persona = persona

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
        pprint(f"{field}: {line}")
