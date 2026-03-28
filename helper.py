import os
import platform
import subprocess
import shutil

def spawn(task_name, command):
    try:
        system = platform.system()

        if system == "Linux":
            # Prefer GNOME Terminal if available
            if shutil.which("gnome-terminal"):
                subprocess.Popen([
                    "gnome-terminal",
                    "--",
                    "bash",
                    "-c",
                    command
                ])
            else:
                # Fallback to xterm
                subprocess.Popen(["xterm", "-e", command])
        if system == "Windows":
            subprocess.Popen(f"cmd /k {command}", shell=True)
            return True
            subprocess.Popen(ps_command, shell=True)
        else:
            print("Unsupported operating system.")
            return False

        return True

    except Exception as e:
        print(f"Error spawning terminal: {e}")
        return False


# spawn("graffiti", """
# echo 'starting street art'
# sleep 1
# python3 streetart.py
# """)