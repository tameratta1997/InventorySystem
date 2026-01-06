$WshShell = New-Object -ComObject WScript.Shell
$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "InventoryServer.lnk"

# Fast Mode Target
$TargetFile = "C:\Windows\System32\cmd.exe"
$Arguments = '/k "C:\Users\Temo\Desktop\Inventory\fast_start_server.bat"'
$WorkingDir = "C:\Users\Temo\Desktop\Inventory"
$IconFile = "C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"

Write-Host "Updating Startup Shortcut at: $ShortcutPath"

try {
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetFile
    $Shortcut.Arguments = $Arguments
    $Shortcut.WorkingDirectory = $WorkingDir
    $Shortcut.IconLocation = $IconFile
    $Shortcut.WindowStyle = 1
    $Shortcut.Description = "Inventory Server (Fast Mode)"
    $Shortcut.Save()
    Write-Host "Success."
}
catch {
    Write-Error "Failed: $_"
}
