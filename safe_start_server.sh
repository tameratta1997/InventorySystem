#!/bin/bash

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_NAME="venv_prod"
PYTHON_VERSION="3.11" # Using python 3.11 for stability

echo "=========================================="
echo "   Inventory System Safe Startup Script   "
echo "=========================================="

# 1. Switch to project directory
cd "$PROJECT_DIR" || exit
echo "[INFO] Working directory: $PROJECT_DIR"

# 2. Check/Create Environment
if [ ! -d "$VENV_NAME" ]; then
    echo "[INFO] Creating new virtual environment '$VENV_NAME'..."
    # Try to find python 3.11, default to python3 if not found
    if command -v python3.11 &> /dev/null; then
         python3.11 -m venv "$VENV_NAME"
    else
         echo "[WARN] Python 3.11 not found, using default python3."
         python3 -m venv "$VENV_NAME"
    fi
else
    echo "[INFO] Virtual environment '$VENV_NAME' exists."
fi

# 3. Activate Environment
source "$VENV_NAME/bin/activate"
echo "[INFO] Environment activated: $(python --version)"

# 4. Install Dependencies
if [ -f "requirements.txt" ]; then
    echo "[INFO] Checking dependencies..."
    pip install -r requirements.txt --quiet
else
    echo "[ERROR] requirements.txt not found! Exiting."
    exit 1
fi

# 5. Run Migrations & Static Files
echo "[INFO] Running database migrations..."
python "$BACKEND_DIR/manage.py" migrate

echo "[INFO] Collecting static files..."
python "$BACKEND_DIR/manage.py" collectstatic --noinput

# 6. Start Server
echo "[INFO] Starting server..."
echo "You can access the server at: http://127.0.0.1:8000/"

# Use gunicorn if available (Production), else fallback to runserver (Dev)
if pip show gunicorn &> /dev/null; then
    echo "[INFO] Using Gunicorn (Production Mode)"
    # We bind to 0.0.0.0 to allow external access (e.g. Tailscale) if needed
    cd "$BACKEND_DIR"
    gunicorn --workers 3 --bind 0.0.0.0:8000 backend.wsgi:application
else
    echo "[INFO] Using Django Runserver (Development Mode)"
    python "$BACKEND_DIR/manage.py" runserver 0.0.0.0:8000
fi
