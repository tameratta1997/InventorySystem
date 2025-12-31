#!/bin/bash

# ==========================================
#    Inventory System FAST START Script
# ==========================================

# Configuration
PROJECT_DIR="/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/InventorySystem"
BACKEND_DIR="$PROJECT_DIR/backend"
CONDA_PYTHON="/opt/anaconda3/envs/inventory_system/bin/python"
CONDA_GUNICORN="/opt/anaconda3/envs/inventory_system/bin/gunicorn"

echo "🚀 Starting Inventory Server in High Performance Mode..."

# 1. Enter Backend Directory
cd "$BACKEND_DIR" || exit

# 2. Check for Tailscale Certificates
CERT_FILE="tamers-macbook-pro.tail9125c6.ts.net.crt"
KEY_FILE="tamers-macbook-pro.tail9125c6.ts.net.key"

if [ -f "$CERT_FILE" ] && [ -f "$KEY_FILE" ]; then
    echo "🔒 SSL Detected. Starting Secure Server (Gunicorn)..."
    # Run with 4 workers for maximum speed/parallelism
    "$CONDA_GUNICORN" \
        --workers 4 \
        --bind 0.0.0.0:8000 \
        --certfile="$CERT_FILE" \
        --keyfile="$KEY_FILE" \
        --preload \
        backend.wsgi:application
else
    echo "⚡ SSL not found. Starting Standard Server (Gunicorn)..."
    "$CONDA_GUNICORN" \
        --workers 4 \
        --bind 0.0.0.0:8000 \
        --preload \
        backend.wsgi:application
fi
