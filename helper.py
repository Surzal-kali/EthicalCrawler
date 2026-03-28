import os
import platform
import subprocess

def spawn(): 
    try:
        if platform.system() == "Linux":
            #Requires xdotool
            subprocess.run(["xdotool", "windowactivate"])
        elif platform.system() == "Darwin": ####i have no idea if this works nor do i plan to test it quite yet. feel free to get your choice of error messages
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