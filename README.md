# 🏪 Quick Commerce - Cửa Hàng Tiện Lợi

Dự án website cửa hàng tiện lợi với mô hình Quick Commerce, hỗ trợ đặt hàng online, quản lý kho hàng, và bán hàng đa kênh.

![Version](https://img.shields.io/badge/version-2.0.0--phase2-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-teal)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)

## 📋 Mục Lục

- [Tính Năng](#tính-năng)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)

---

## ✨ Tính Năng

### Phase 1 ✅ Database & Mock Data
- PostgreSQL với Docker
- Schema FEFO (First Expired First Out)
- 78 sản phẩm, 10 danh mục (tiếng Việt)
- Script cào ảnh sản phẩm

### Phase 2 ✅ Backend API
- FastAPI RESTful API
- JWT Authentication
- Role-based Access Control (Customer, Staff, Admin)
- CRUD: Categories, Products, Users
- Inventory Management với FEFO & Pessimistic Locking
- Order Processing với Stock Allocation
- Alembic Migrations

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **API** | FastAPI + Uvicorn |
| **Database** | PostgreSQL 16 (async) |
| **ORM** | SQLAlchemy 2.0 + asyncpg |
| **Cache** | Redis 7 |
| **Auth** | JWT (python-jose) |
| **Container** | Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Git

### Run

```powershell
# Clone
git clone <repo-url>
cd Web_Shop

# Start all services
docker-compose up -d

# Wait for services...
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs
# Adminer: http://localhost:8080
```

### Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@shop.vn | password123 | Admin |
| staff1@shop.vn | password123 | Staff |
| khach1@gmail.com | password123 | Customer |

---

## 📚 API Documentation

### Endpoints Summary

| Module | Prefix | Endpoints |
|--------|--------|-----------|
| Auth | `/api/v1/auth` | register, login, refresh, me |
| Users | `/api/v1/users` | CRUD (admin only) |
| Categories | `/api/v1/categories` | list, get, create, update, delete |
| Products | `/api/v1/products` | list, get, create, update, delete, upload image |
| Inventory | `/api/v1/inventory` | overview, batches, low-stock, expiring |
| Cart | `/api/v1/cart` | get, add, update, remove, clear |
| Orders | `/api/v1/orders` | list, get, create, update status, cancel |

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
Web_Shop/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── alembic/                  # Migrations
├── database/
│   ├── init.sql
│   └── mock_data.sql
├── src/
│   ├── main.py              # FastAPI app
│   ├── core/                # Config, DB, Security
│   ├── models/              # All models registry
│   ├── auth/                # Authentication
│   ├── users/               # Users CRUD
│   ├── catalog/             # Categories, Products
│   ├── inventory/           # FEFO, Locking
│   └── orders/              # Cart, Orders
└── scripts/                 # Utilities
```

---

## 🔧 Commands

```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f backend

# Run migrations
docker exec -it shop_backend alembic upgrade head

# Database shell
docker exec -it shop_db psql -U shop_user -d shop_db
```

---

## 📖 Documentation

- [GUIDE.md](./GUIDE.md) - Hướng dẫn chi tiết

---

Made with ❤️ for DNU Web Development Course
