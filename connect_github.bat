@echo off
echo [INFO] Connecting to GitHub...

:: Check for GitHub CLI
where gh >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] GitHub CLI (gh) not found. 
    echo Please restart your terminal/PC if you just installed it.
    pause
    exit /b
)

echo.
echo [INSTRUCTION] A browser window will open to authorize this computer.
echo.
gh auth login -p https -w

echo.
echo [INFO] Connection check:
gh auth status

pause
