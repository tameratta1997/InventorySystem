#!/bin/bash
# Inventory System Startup Script

# Navigate to the backend directory
cd /Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/InventorySystem/backend

# Run the server using the virtual environment's python
# Binding to 0.0.0.0 allows access from other devices on the network
/Users/tamerelwakeel/Documents/Python_Projects/Python_Diploma/InventorySystem/venv/bin/python manage.py runserver 0.0.0.0:8000
