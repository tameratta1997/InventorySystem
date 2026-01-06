$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Start Inventory.lnk"

# Target paths
$TargetFile = "C:\Users\Temo\Desktop\Inventory\safe_start_server.bat"
$WorkingDir = "C:\Users\Temo\Desktop\Inventory"
$IconFile = "C:\Users\Temo\Desktop\Inventory\inventory_icon.ico"

Write-Host "Creating shortcut at: $ShortcutPath"
Write-Host "Target: $TargetFile"
Write-Host "Icon: $IconFile"

try {
    # Create or Overwrite Shortcut
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetFile
    $Shortcut.WorkingDirectory = $WorkingDir
    $Shortcut.IconLocation = $IconFile
    $Shortcut.WindowStyle = 1 # 1 = Normal, 7 = Minimized
    $Shortcut.Description = "Start Inventory Server"
    $Shortcut.Save()
    
    Write-Host "Shortcut saved successfully."

    # Verification
    Start-Sleep -Seconds 1
    $VerifyShortcut = $WshShell.CreateShortcut($ShortcutPath)
    Write-Host "--- Verification ---"
    Write-Host "Target: $($VerifyShortcut.TargetPath)"
    Write-Host "Icon: $($VerifyShortcut.IconLocation)"
} catch {
    Write-Error "Failed to create shortcut: $_"
    exit 1
}
