import winreg

def disable_teams_startup():
    path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        # 1. Open Key with Write permissions
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
        
        # 2. Delete the value
        try:
            winreg.DeleteValue(key, "Teams")
            print("Successfully deleted 'Teams' from HKCU...Run")
        except FileNotFoundError:
            print("'Teams' not found in Run key (already deleted?)")
            
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"Error accessing registry: {e}")

if __name__ == "__main__":
    disable_teams_startup()
