import os
import platform
import subprocess
import shutil

def spawn(task_name, command):
    try:
        system = platform.system()

        if system == "Linux":
            # Kali default terminal
            if shutil.which("xfce4-terminal"):
                subprocess.Popen([
                    "xfce4-terminal",
                    "--command",
                    command
                ])
            else:
                # Fallback for ultra-minimal systems
                subprocess.Popen(["xterm", "-e", command])
        if system == "Windows":
            subprocess.Popen(f"cmd /k {command}", shell=True)
            return True

    except Exception as e:
        print(f"Error spawning terminal: {e}")
        pass


# spawn("graffiti", """
# echo 'starting street art'
# sleep 1
# python3 streetart.py
# """)