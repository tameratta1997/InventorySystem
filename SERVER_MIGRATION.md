# 🚚 Inventory Server Migration Guide

Follow these steps to move your Inventory System to a new computer.

## 1. Prepare the New Computer
1.  **Install Python**: Download and install the latest Python from [python.org](https://python.org).
2.  **Install Git**: Download and install Git from [git-scm.com](https://git-scm.com).

## 2. Get the Code
Open a terminal on the new computer and run:
```bash
git clone https://github.com/tameratta1997/iPad-Graphing-Calculator.git
cd iPad-Graphing-Calculator/InventorySystem
```

## 3. Transfer Your Data (Important!)
The database and images are **not** stored in the cloud (GitHub) for security and size reasons. You must copy them manually from the old computer.

**From Old Computer:**
1.  Locate `InventorySystem/backend/db.sqlite3` (This is your database).
2.  Locate the `InventorySystem/backend/media` folder (This contains product images).

**To New Computer:**
1.  Place `db.sqlite3` into `InventorySystem/backend/` on the new machine.
2.  Place the `media` folder into `InventorySystem/backend/` on the new machine.

## 4. Install Dependencies
On the new computer terminal (inside `InventorySystem` folder):

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 5. Start the Server
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

## 6. Connect
1.  Find the **Local IP Address** of the new computer.
    *   **Mac**: System Settings -> Network -> Wi-Fi -> Details...
    *   **Windows**: Open CMD, type `ipconfig`.
2.  On other devices, enter: `http://<NEW_IP_ADDRESS>:8000`

## 7. (Optional) Auto-Start on Mac
If the new computer is a Mac, you can enable auto-start again:
```bash
# Edit the plist file to update paths if your username is different!
nano com.tamer.inventory.plist 

# Then copy and load it
cp com.tamer.inventory.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.tamer.inventory.plist
```
