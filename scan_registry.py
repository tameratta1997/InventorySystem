import winreg

def list_registry_startup():
    keys = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"),
    ]

    found = []

    for root, path in keys:
        try:
            with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        print(f"[{path}] {name} = {value}")
                        if "teams" in name.lower() or "teams" in str(value).lower():
                            found.append((root, path, name))
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            pass
        except PermissionError:
            print(f"Permission denied for {path}")
            
    return found

if __name__ == "__main__":
    print("Scanning Registry for Startup items...")
    found_items = list_registry_startup()
    print("\n--- Potential Teams Hits ---")
    for item in found_items:
        print(item)
