@echo off
setlocal

:: Configuration
set VENV_NAME=venv_prod

echo ==========================================
echo    Inventory System Windows Startup
echo ==========================================

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

:: 3. Install dependencies
echo [INFO] Checking/Installing dependencies...
pip install -r requirements.txt --quiet

:: 4. Run migrations
echo [INFO] Running database migrations...
python backend\manage.py migrate

:: 5. Collect static files
echo [INFO] Collecting static files...
python backend\manage.py collectstatic --noinput

:: 6. Start server
echo ==========================================
echo [INFO] Starting server...
echo Access the system at: http://127.0.0.1:8000/
echo ==========================================
python backend\manage.py runserver 0.0.0.0:8000

pause
