@echo off
setlocal

:: Configuration
set VENV_NAME=venv_prod

echo ==========================================
echo    Inventory System Windows Startup
echo ==========================================

:: 0. Auto-Add to Startup Folder
echo [INFO] Ensuring server starts with Windows...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SCRIPT_PATH=%~f0"
set "SHORTCUT_PATH=%STARTUP_DIR%\InventoryServer.lnk"

if not exist "%SHORTCUT_PATH%" (
    powershell -ExecutionPolicy Bypass -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
    echo [OK] Added to Windows Startup.
)

:: 1. Check if virtual environment exists
if not exist "%VENV_NAME%" (
    echo [INFO] Creating new virtual environment "%VENV_NAME%"...
    python -m venv %VENV_NAME%
    if errorlevel 1 (
        echo [ERROR] Python not found or failed to create venv. 
        echo Please ensure Python is installed and added to PATH.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Virtual environment "%VENV_NAME%" exists.
)

:: 2. Activate environment
echo [INFO] Activating environment...
call %VENV_NAME%\Scripts\activate

:: 3. Upgrade Pip
echo [INFO] Upgrading Pip...
python -m pip install --upgrade pip --quiet --trusted-host pypi.org --trusted-host files.pythonhosted.org

:: 4. Install dependencies
echo [INFO] Checking/Installing dependencies...
pip install -r requirements.txt --quiet

:: 4. Run migrations
echo [INFO] Running database migrations...
python backend\manage.py migrate

:: 5. Collect static files
echo [INFO] Collecting static files...
python backend\manage.py collectstatic --noinput

:: 6. Database Backup (Crash Protection)
if not exist "backups" mkdir backups
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
echo [INFO] Backing up database...
copy backend\db.sqlite3 backups\db_backup_%TIMESTAMP%.sqlite3 >nul

:: 7. Start server
echo ==========================================
echo [INFO] Starting server...
echo Access the system at: http://127.0.0.1:8000/
echo ==========================================
python backend\manage.py runserver 0.0.0.0:8000

pause
