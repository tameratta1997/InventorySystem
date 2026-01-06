$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Start Inventory.lnk"

# Target paths
$TargetFile = "C:\Users\Temo\Desktop\Inventory\safe_start_server.bat"
$WorkingDir = "C:\Users\Temo\Desktop\Inventory"
$IconFile = "C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"

Write-Host "Re-creating shortcut at: $ShortcutPath"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.IconLocation = $IconFile
$Shortcut.WindowStyle = 1
$Shortcut.Save()

Write-Host "Done."
