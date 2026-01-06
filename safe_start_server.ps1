# safe_start_server.ps1 - Fast Windows Startup Script for Inventory App

# Set Error Action to Stop on errors
$ErrorActionPreference = "Stop"

# Determine script directory
$SCRIPT_DIR = $PSScriptRoot
$BACKEND_DIR = Join-Path $SCRIPT_DIR "backend"

Write-Host "[INFO] Starting Inventory Server (Fast Mode)..." -ForegroundColor Green

# 1. Start Server Directly
# We skip migration/requirements checks for speed. 
# Run them manually if you update the code!

Write-Host "[INFO] Starting server on Port 8000..." -ForegroundColor Green
Write-Host "Tailscale Secure Address: https://minint-5rjphna.tail9125c6.ts.net/" -ForegroundColor Cyan

# Force standard HTTP runserver. Tailscale Serve proxies 443 -> 8000.
# We assume python is in PATH.
try {
    python "$BACKEND_DIR\manage.py" runserver 0.0.0.0:8000
}
catch {
    Write-Error "Failed to start server. Ensure Python is in PATH and backend/manage.py exists."
    exit 1
}
