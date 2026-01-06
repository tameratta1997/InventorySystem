import os
import winshell
import sys

startup_dir = winshell.startup()
print(f"Startup Directory: {startup_dir}")

try:
    files = os.listdir(startup_dir)
    print("Files in startup:", files)
    
    for f in files:
        if f.endswith(".lnk"):
            full_path = os.path.join(startup_dir, f)
            try:
                shortcut = winshell.shortcut(full_path)
                print(f"Shortcut: {f}")
                print(f"  Target: {shortcut.path}")
                print(f"  Args: {shortcut.arguments}")
                print(f"  WorkingDir: {shortcut.working_directory}")
            except Exception as e:
                print(f"  Error reading shortcut {f}: {e}")

except Exception as e:
    print(f"Error checking startup dir: {e}")
