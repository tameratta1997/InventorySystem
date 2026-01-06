import os
import winshell
from win32com.client import Dispatch

def update_startup_shortcut():
    startup_dir = winshell.startup()
    shortcut_path = os.path.join(startup_dir, "InventoryServer.lnk")
    
    target_bat = r"C:\Users\Temo\Desktop\Inventory\fast_start_server.bat"
    icon = r"C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"
    working_dir = r"C:\Users\Temo\Desktop\Inventory"
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    
    # Configure for Fast Startup (cmd /k to keep open)
    shortcut.TargetPath = r"C:\Windows\System32\cmd.exe"
    shortcut.Arguments = f'/k "{target_bat}"'
    shortcut.WorkingDirectory = working_dir
    shortcut.IconLocation = icon
    shortcut.WindowStyle = 1 # Normal
    shortcut.Description = "Inventory Server (Fast Mode)"
    
    shortcut.Save()
    print(f"Updated Startup Shortcut at: {shortcut_path}")
    print(f"Target: {shortcut.TargetPath} {shortcut.Arguments}")

if __name__ == "__main__":
    update_startup_shortcut()
