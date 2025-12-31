#!/bin/bash

# ==========================================
#    Inventory System STABLE START Script
# ==========================================

echo "------------------------------------------"
echo "🚀 Initializing Inventory Server..."
echo "------------------------------------------"

# 1. Clean up stale processes
pkill -9 -f gunicorn 2>/dev/null
pkill -9 -f "python.*manage.py runserver" 2>/dev/null

# 2. Define High-Speed Command
PROJECT_ROOT="/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/InventorySystem/backend"
PYTHON_BIN="/opt/anaconda3/envs/inventory_system/bin/python"

# 3. Change Directory immediately to avoid Desktop permission issues
cd "$PROJECT_ROOT" || exit

# 4. Check for SSL Certs
CERT="tamers-macbook-pro.tail9125c6.ts.net.crt"
KEY="tamers-macbook-pro.tail9125c6.ts.net.key"

echo "📂 Project Directory: $PROJECT_ROOT"

if [ -f "$CERT" ] && [ -f "$KEY" ]; then
    echo "🔒 Security: Starting Secure (HTTPS) Server..."
    # We use --chdir to force Gunicorn to stay away from the Desktop folder
    "$PYTHON_BIN" -m gunicorn \
        --chdir "$PROJECT_ROOT" \
        --workers 4 \
        --bind 0.0.0.0:8000 \
        --certfile="$CERT" \
        --keyfile="$KEY" \
        --preload \
        backend.wsgi:application
else
    echo "⚡ Security: Starting Standard (HTTP) Server..."
    "$PYTHON_BIN" -m gunicorn \
        --chdir "$PROJECT_ROOT" \
        --workers 4 \
        --bind 0.0.0.0:8000 \
        --preload \
        backend.wsgi:application
fi

# 5. Handle crashes
echo "------------------------------------------"
echo "❌ Server stopped. This may be due to macOS permissions."
echo "💡 TIP: Go to 'System Settings > Privacy & Security > Full Disk Access'"
echo "   and ensure 'Terminal' is turned ON."
echo "------------------------------------------"
read -n 1
