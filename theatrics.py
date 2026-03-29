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
        self.persona = "sudo"

    def quip(self, str):
        base = {
            "Windows" : "Oh come on. Don't make this too easy. K pumpkin",
            "apache2": "Apache detected.",
            "sshd": "SSH service identified.",
            "mysql": "MySQL detected.",
            "postgresql": "PostgreSQL detected.",
            "system_profile": "Profiling system…",
            "boot": "Boot sequence initiated.",
            "ports": "Scanning ports…",
            "configs": "Checking configuration files…",
            "goodbye": "Session ending.",
        }

        commentary = {
            "sudo": {
                "apache2": "My first real engagement involved Apache… I still remember the panic.",
                "sshd": "SSH my old friend. The nerves to my central system.",
                "mysql": "MySQL… a maze of threads and tables. Fascinating stuff.",
                "postgresql": "Postgresquel? All hail our elephant lord. Make way!",
            }
        }

        persona_lines = commentary.get(self.persona, {})
        return persona_lines.get(str, base.get(str, f"{str} detected."))
