# Server Migration Guide

This guide explains how to move the Inventory System to a new computer.

## Strategy A: The Professional Way (Recommended)
The best way to migrate is using **Git** for code and manually moving the **Database**.

### 1. Code Migration
On the new PC, clone your repository:
```bash
git clone https://github.com/tameratta1997/InventorySystem.git
cd InventorySystem
```

### 2. Physical Data Migration
Copy these files/folders from the old PC to the new PC manually (via USB or Network):
- `backend/db.sqlite3` (Your real data: products, sales, users)
- `backend/media/` (Any uploaded images or files)

### 3. Setup on New PC
1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR venv\Scripts\activate # Windows
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Secure with Tailscale**:
   - Install Tailscale and log in.
   - Run: `tailscale cert your-new-pc-name.ts.net` (Update the startup script with the new name).

---

## Strategy B: The Zip File Way
If you prefer using a Zip file, use the one I generated: `InventorySystem_Migration.zip`.

1. **Unzip** the folder on the new PC.
2. Follow the **Setup on New PC** steps above.

### Important Note on Security
The SSL certificates (`.crt` and `.key`) are specific to each computer. You **must** generate new ones on the new PC using Tailscale for the security lock to work correctly.
