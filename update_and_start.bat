@echo off
setlocal

:: Configuration
set VENV_NAME=venv_prod

echo ==========================================
echo    Inventory System - UPDATE & START
echo ==========================================

:: 1. Check/Create Environment
if not exist "%VENV_NAME%" (
    echo [INFO] Creating new virtual environment "%VENV_NAME%"...
    python -m venv %VENV_NAME%
)

:: 2. Activate
set PYTHON_EXE=%VENV_NAME%\Scripts\python.exe
set PIP_EXE=%VENV_NAME%\Scripts\pip.exe

:: 3. Install Requirements
echo [INFO] Updating dependencies...
"%PIP_EXE%" install -r requirements.txt --quiet

:: 4. Run Migrations (CRITICAL: DB Schema Changed)
echo [INFO] Updating Database Schema (Migrations)...
"%PYTHON_EXE%" backend\manage.py makemigrations --noinput
echo [INFO] Applying Migrations...
"%PYTHON_EXE%" backend\manage.py migrate --noinput

:: 5. Create Default Store (Migration Logic help)
:: We create a simple script to ensure 'Main Store' exists for old data
echo [INFO] Validating Store Configuration...
"%PYTHON_EXE%" -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings'); django.setup(); from inventory.models import Store; Store.objects.get_or_create(name='Main Store', defaults={'location': 'Default'})"

:: 6. Start Server (Standard Mode)
echo ==========================================
echo [INFO] Starting Server...
"%PYTHON_EXE%" backend\manage.py runserver 0.0.0.0:8000

pause
