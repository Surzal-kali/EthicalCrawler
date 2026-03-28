import os
import platform
import subprocess

def activate_terminal(): 
    try:
        if platform.system() == "Linux":
            #Requires xdotool
            subprocess.run(["xdotool", "windowactivate", "--name", "EthicalCrawler"])
        elif platform.system() == "Darwin":
            subprocess.run(["osascript", "-e", 'tell application "System Events" to tell process "Terminal" to set frontmost to true'])
        elif platform.system() == "Windows":
            import ctypes
            hwnd = ctypes.windll.user32.FindWindowW(None, "EthicalCrawler")
            if hwnd:
                ctypes.windll.kernel32.SetForegroundWindow(hwnd)
        else:
            print("Unsupported operating system.")
            return False
        return True
    except Exception as e:
        print(f"Error activating terminal: {e}")
        return False