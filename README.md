# Inventory Management System

A complete, scalable Inventory Management System built with Python Django.
Features: Product Management, Stock Alerts, Dashboard, REST API, "Premium" UI.

## Tech Stack
- **Backend Framework**: Django 6.0 (Python)
- **Database**: SQLite (Dev) / PostgreSQL (Prod ready)
- **Frontend**: Django Templates + Vanilla CSS (Premium Design) via `static/css`.
- **API**: Django Rest Framework (DRF)

## Project Structure
```
InventorySystem/
├── backend/            # Django Project Root
│   ├── inventory/      # Main App (Models, Views, API)
│   ├── templates/      # HTML Templates (Dashboard, Products)
│   ├── static/         # CSS/Images
│   ├── manage.py       # Entry point
├── venv/               # Python Virtual Environment
├── DESIGN.md           # Architecture Design Doc
```

## Quick Start

1. **Navigate to Project Directory**
   ```bash
   cd InventorySystem
   ```
   *(Ensure you are in `InventorySystem`)*

2. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers pillow
   ```

4. **Run Migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

5. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Server**
   ```bash
   python manage.py runserver
   ```
   Access the app at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Usage
The system provides a REST API for mobile integration.
- Products: `GET /api/products/`
- Categories: `GET /api/categories/`

## Deployment (Production)
For production deployment, we recommend Docker.
1. Use `gunicorn` as the WSGI server.
2. Use `nginx` to serve static files and proxy requests.
3. Set `DEBUG=False` in `settings.py`.
4. Switch Database to PostgreSQL.

### Sample Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```
