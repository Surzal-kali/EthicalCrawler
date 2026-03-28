import os
import platform
import subprocess

def spawn(task_name, command):
    try:
        system = platform.system()

        if system == "Linux":
            subprocess.Popen(["xterm", "-e", f"bash -c \"{command}\""])
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