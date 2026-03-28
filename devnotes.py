from helper import spawn
import time


def streetart(terminal_name=None):
    """Displays the street art messages."""
    if terminal_name:
        spawn()  # Bring terminal to foreground

    messages = [
        "my secrets on how i do this can be parsed from the logs and code\n",
        "instead lets focus on having some fun\n",
        "I've always heard from people with no sense that hacking is street art\n",
        "So lets make street art\n"
    ]
    for message in messages:
        for char in message:
            print(char, end='', flush=True)
            time.sleep(0.03)

