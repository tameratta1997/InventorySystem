# Inventory Management System - Design & Architecture

## 1. Tech Stack Justification

### Backend: Python Django
- **Reasoning**: Django is a "batteries-included" framework perfect for complex database-driven applications like Inventory Systems. it includes:
    - **Admin Interface**: Instant access to manage data (Users, Products) for Admins.
    - **ORM**: Secure and scalable database abstraction.
    - **Authentication**: Built-in robust user management and permissions.
    - **Security**: Protection against common attacks (SQL Injection, XSS, CSRF) by default.
- **Scalability**: Can handle high traffic and integrates well with ML/AI libraries if needed later.

### Frontend: React + Vite
- **Reasoning**: React is the industry standard for dynamic web applications.
    - **Component-Based**: Perfect for reusable UI elements (Product Cards, Tables, Forms).
    - **Ecosystem**: rich library of chart tools (Recharts) and icons (Lucide/Heroicons).
    - **Vite**: Ultra-fast build tool for a smooth development experience.
- **Styling**: Vanilla CSS with CSS Variables for a custom, high-performance "Premium" look.

### Database: PostgreSQL
- **Reasoning**: Robust, open-source relational database. Handles complex queries and transactions (ACID compliance) which are critical for financial/stock data.
- *Note: For this initial local setup, we may use SQLite for simplicity, but the code is 100% compatible with PostgreSQL.*

---

## 2. Database Schema (ERD)

### Users (Built-in Django User)
- `id`: PK
- `username`: String
- `role`: Enum (Admin, Staff, Viewer)
- `password_hash`: String

### Category
- `id`: PK
- `name`: String (Unique)
- `slug`: String
- `description`: Text

### Supplier
- `id`: PK
- `name`: String
- `email`: String
- `phone`: String
- `address`: Text

### Product
- `id`: PK
- `code`: String (Unique, Indexed) - *For barcode*
- `name`: String (Indexed)
- `category`: FK -> Category
- `supplier`: FK -> Supplier (Nullable)
- `purchase_price`: Decimal
- `selling_price`: Decimal
- `quantity`: Integer (Default 0)
- `min_stock_alert`: Integer (Default 10)
- `description`: Text
- `image`: ImageField (Path to file)
- `created_at`: DateTime
- `updated_at`: DateTime

### Transaction
- `id`: PK
- `type`: Enum (SALE, PURCHASE)
- `user`: FK -> User
- `total_amount`: Decimal
- `date`: DateTime

### TransactionItem
- `id`: PK
- `transaction`: FK -> Transaction
- `product`: FK -> Product
- `quantity`: Integer
- `price_at_moment`: Decimal (Snapshot of price)

### StockLog (Audit)
- `id`: PK
- `product`: FK -> Product
- `user`: FK -> User
- `change_quantity`: Integer (+/-)
- `reason`: String
- `timestamp`: DateTime

---

## 3. Deployment Strategy
1. **Containerization**: Docker & Docker Compose to orchestrate Django (Backend) + React (Frontend - Nginx) + PostgreSQL.
2. **Environment API**: Backend serves REST API at `/api/`. Frontend consumes it.

## 4. Key Features Implemented (Plan)
- **Role-Based Access**: implemented via Django Groups/Permissions.
- **Stock alerts**: implemented via simple logic checking `quantity <= min_stock_alert`.
- **Image Handling**: Django Media files.
