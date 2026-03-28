import os
import platform
import subprocess
import shutil

def spawn(task_name, command):
    try:
        system = platform.system()
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get directory of helper.py
        main_script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get the directory one level up for where the main script is.

        if system == "Linux":
            # Kali default terminal
            if shutil.which("qterminal"):
                subprocess.Popen([
                    "qterminal",
                    "--command",
                    f"cd {main_script_dir} && {command}"  # Change directory before executing command
                ])
            else:
                # Fallback for ultra-minimal systems
                subprocess.Popen(["xterm", "-e", f"cd {main_script_dir} && {command}"])
        elif system == "Windows":
            subprocess.Popen(f"cmd /k cd /d {main_script_dir} && {command}", shell=True)  # cd /d for changing drive
        else:
            print("Unsupported operating system.")
            return False

    except Exception as e:
        print(f"Error spawning terminal: {e}")
        return False
