$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Start Inventory.lnk"

# Target paths
$TargetFile = "C:\Windows\System32\cmd.exe"
$Arguments = '/k "C:\Users\Temo\Desktop\Inventory\fast_start_server.bat"'
$WorkingDir = "C:\Users\Temo\Desktop\Inventory"
$IconFile = "C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"

Write-Host "Updating shortcut to Fast Mode at: $ShortcutPath"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetFile
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.IconLocation = $IconFile
$Shortcut.WindowStyle = 1
$Shortcut.Description = "Start Inventory Server (Fast Mode)"
$Shortcut.Save()

Write-Host "Shortcut updated successfully."
