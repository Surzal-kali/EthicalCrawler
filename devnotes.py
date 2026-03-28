from helper import spawn
import time

def notes(terminal_name=None):
    if terminal_name:
        # Spawn a new terminal to display the street art
        spawn(terminal_name, "python3 -c \"from devnotes import streetart; streetart()\"")
        return
    
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
        time.sleep(0.5) #####dramatic ain't it?
    
    print("\n" + "="*60)
if __name__ == "__main__":
    notes()