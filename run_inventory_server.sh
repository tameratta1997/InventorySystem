#!/bin/bash
# Inventory System Startup Script (SSL Secured via Tailscale)

# Navigate to the backend directory
cd /Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/InventorySystem/backend

# Define Certificate paths
CERT_FILE="tamers-macbook-pro.tail9125c6.ts.net.crt"
KEY_FILE="tamers-macbook-pro.tail9125c6.ts.net.key"

# Check if certs exist, if not try to get them
if [ ! -f "$CERT_FILE" ]; then
    echo "SSL Certificate not found, attempting to retrieve from Tailscale..."
    /Applications/Tailscale.app/Contents/MacOS/Tailscale cert tamers-macbook-pro.tail9125c6.ts.net
fi

# Run the server using Gunicorn for production-grade SSL support
# Binding to 0.0.0.0 allows access from other devices on the Tailscale network
../venv/bin/gunicorn --certfile="$CERT_FILE" --keyfile="$KEY_FILE" --bind 0.0.0.0:8000 backend.wsgi:application
