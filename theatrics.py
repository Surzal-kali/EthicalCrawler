import time
def pspace(message, char_delay=0.03, line_delay=0.5):
    print("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")

def pprint(message, char_delay=0.03, line_delay=0.5):
    print("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print("\n")


class Me:
    def __init__(self):
        self.persona = "foothold"

    def quip(self, str):
        base = { #### Something broke man idk just paste
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

        commentary = {
    "foothold": { ####Creeping Closer
        "Windows": "Windows??? Oh don't make this too easy now",
        "Linux": "linux huh??? this is where it gets interesting",
        "apache2": "My first real engagement involved Apache… I still remember the panic.",
        "sshd": "SSH my old friend. The nerves to my central system.",
        "mysql": "MySQL… a maze of threads and tables. Fascinating stuff.",
        "postgresql": "Postgresquel? All hail our elephant lord. Make way!",
    },
    "sudo": { #########HI BUD
        "Windows": "[SUDO] Elevated access on Windows. Time to dig deeper.",
        "Linux": "[SUDO] Root's power. Let's see what we can find.",
        "apache2": "[SUDO] Apache configs are fully readable now.",
        "sshd": "[SUDO] SSH host keys accessible. Interesting...",
        "mysql": "[SUDO] Dumping MySQL credentials? Don't mind if I do.",
        "postgresql": "[SUDO] PostgreSQL - time to enumerate databases.",
        "system_profile": "[SUDO] Full system profile. No secrets left.",
        "boot": "[SUDO] Boot sequence with elevated privileges.",
        "ports": "[SUDO] All ports visible, even filtered ones.",
        "configs": "[SUDO] Every config file is now readable.",
        "goodbye": "[SUDO] Shutting down elevated session.",
    }
}

        persona_lines = commentary.get(self.persona, {})
        
        # Return a SINGLE string: persona first, then base, then fallback
        return persona_lines.get(str, base.get(str, f"{str} detected."))