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

:: 0.1 Kill Existing Server (Port 8000)
echo [INFO] checking for existing server instances...
powershell -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force; Write-Host 'Stopped existing process' }"

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
set PYTHON_EXE=%VENV_NAME%\Scripts\python.exe
set PIP_EXE=%VENV_NAME%\Scripts\pip.exe

:: 3. Upgrade Pip
echo [INFO] Upgrading Pip...
"%PYTHON_EXE%" -m pip install --upgrade pip --quiet --trusted-host pypi.org --trusted-host files.pythonhosted.org

:: 4. Install dependencies
echo [INFO] Checking/Installing dependencies...
"%PIP_EXE%" install -r requirements.txt --quiet --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host files.pythonhosted.org

:: 5. Run migrations
echo [INFO] Syncing database changes...
"%PYTHON_EXE%" backend\manage.py makemigrations --noinput
"%PYTHON_EXE%" backend\manage.py migrate --noinput

:: 5.1 Ensure Default Store (Multi-Store Support)
echo [INFO] Validating Store Setup...
"%PYTHON_EXE%" -c "import sys, os; sys.path.append(os.path.join(os.getcwd(), 'backend')); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings'); import django; django.setup(); from inventory.models import Store; Store.objects.get_or_create(name='Main Store', defaults={'location': 'Default'})"

:: 6. Collect static files
echo [INFO] Collecting static files...
"%PYTHON_EXE%" backend\manage.py collectstatic --noinput

:: 7. Database Backup (Crash Protection)
if not exist "backups" mkdir backups
set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
echo [INFO] Backing up database...
copy backend\db.sqlite3 backups\db_backup_%TIMESTAMP%.sqlite3 >nul

:: 8. Start server
echo ==========================================
echo [INFO] Starting server...

:: 8.1 Try Windows Tailscale Certs
set WIN_CERT=backend\minint-5rjphna.tail9125c6.ts.net.crt
set WIN_KEY=backend\minint-5rjphna.tail9125c6.ts.net.key

:: 8.2 Try Mac Tailscale Certs
set MAC_CERT=backend\tamers-macbook-pro.tail9125c6.ts.net.crt
set MAC_KEY=backend\tamers-macbook-pro.tail9125c6.ts.net.key

if exist "%WIN_CERT%" (
    echo [INFO] Windows SSL Detected...
    set "USE_CERT=minint-5rjphna.tail9125c6.ts.net.crt"
    set "USE_KEY=minint-5rjphna.tail9125c6.ts.net.key"
)

if exist "%MAC_CERT%" (
    echo [INFO] Mac SSL Detected...
    set "USE_CERT=tamers-macbook-pro.tail9125c6.ts.net.crt"
    set "USE_KEY=tamers-macbook-pro.tail9125c6.ts.net.key"
)

if defined USE_CERT (
    echo [INFO] HTTPS Mode Enabled.
    echo Access: https://127.0.0.1:8000/
    echo ==========================================
    cd backend
    ..\venv_prod\Scripts\uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --ssl-certfile="%USE_CERT%" --ssl-keyfile="%USE_KEY%"
    pause
    exit /b
)

echo [WARN] SSL not found. Starting Standard Server (HTTP)...
echo Access the system at: http://127.0.0.1:8000/
echo ==========================================
"%PYTHON_EXE%" backend\manage.py runserver 0.0.0.0:8000

pause
