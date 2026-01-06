@echo off
cd /d "%~dp0"
echo [INFO] Launching Fast Startup Script...
powershell -ExecutionPolicy Bypass -File "safe_start_server.ps1"
if %errorlevel% neq 0 (
    echo [ERROR] Script execution failed.
    pause
    exit /b %errorlevel%
)
pause
