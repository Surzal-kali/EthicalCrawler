import os
import platform
import subprocess

def spawn(task_name, command):
    #just me and your computer, having a nice chat
    try:
        if platform.system() == "Linux":
            subprocess.Popen(["xterm", "-e", command])
        elif platform.system() == "Windows":
            subprocess.Popen(["start", "cmd", "/k", command], shell=True)  # Use shell=True for Windows
        else:
            print("Unsupported operating system.")
            return False  # Indicate failure
        return True  # Indicate success
    except Exception as e:
        print(f"Error spawning terminal: {e}")
        return False  # Indicate failure. my immeasurable dissapointment
