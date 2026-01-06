@echo off
echo [INFO] checking for Git...

set GIT_CMD=git
where git >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%ProgramFiles%\Git\cmd\git.exe" (
        set "GIT_CMD=%ProgramFiles%\Git\cmd\git.exe"
    ) else (
        echo [ERROR] Git is not installed or not in PATH.
        echo Please wait for the installation to finish or install it manually.
        pause
        exit /b 1
    )
)

echo [INFO] Using Git: %GIT_CMD%
echo [INFO] Initializing Repository...
"%GIT_CMD%" init

echo [INFO] configuring User...
"%GIT_CMD%" config user.name "tameratta1997"
"%GIT_CMD%" config user.email "tameratta1997@users.noreply.github.com"

echo [INFO] Adding files...
"%GIT_CMD%" add .

echo [INFO] Committing...
"%GIT_CMD%" commit -m "Initial commit of Inventory System"

echo [INFO] Setting up Remote...
"%GIT_CMD%" remote remove origin >nul 2>nul
"%GIT_CMD%" remote add origin https://github.com/tameratta1997/InventorySystem.git

echo [INFO] Pushing code...
echo [NOTE] You may be asked to sign in.
"%GIT_CMD%" branch -M main
"%GIT_CMD%" push -u origin main

echo [SUCCESS] Done.
pause
