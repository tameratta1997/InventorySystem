===================================================
   Inventory System - Windows Migration Guide
===================================================

Installation Steps:
------------------

1. Python Installation:
   - Ensure Python 3.11 or later is installed.
   - You can download it from: https://www.python.org/downloads/windows/
   - IMPORTANT: During installation, verify that "Add Python to PATH" is checked.

2. Running the Server (Automated):
   - Double-click the `safe_start_server.bat` file.
   - This script will:
     - Create a virtual environment (`venv_prod`).
     - Install all required libraries.
     - Set up the database.
     - Start the server at http://127.0.0.1:8000/

3. Running Manually (If the script fails):
   - Open Command Prompt (cmd) or PowerShell in this folder.
   - Run the following commands:
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     python backend\manage.py migrate
     python backend\manage.py collectstatic --noinput
     python backend\manage.py runserver 0.0.0.0:8000

4. Accessing the System:
   - Open your browser and go to: http://127.0.0.1:8000/
   - Login with your existing credentials (admin).

Note for Docker Users:
----------------------
If you have Docker Desktop installed on Windows, you can simply run:
   docker-compose up --build
This works regardless of Python version installed on your system.

Troubleshooting:
----------------
- If you see "python not found", make sure you added Python to your PATH during installation.
- If images are missing, ensure the 'media' folder was copied correctly.
