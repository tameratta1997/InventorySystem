$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Start Inventory.lnk"

# We use cmd /k to keep window open
$TargetFile = "C:\Windows\System32\cmd.exe"
$Arguments = '/k "C:\Users\Temo\Desktop\Inventory\safe_start_server.bat"'
$WorkingDir = "C:\Users\Temo\Desktop\Inventory"
$IconFile = "C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"

Write-Host "Creating robust shortcut at: $ShortcutPath"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetFile
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.IconLocation = $IconFile
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Start Inventory Server (Persistent Window)"
$Shortcut.Save()

Write-Host "Shortcut updated to use cmd /k."
