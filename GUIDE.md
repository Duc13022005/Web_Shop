# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG

Hướng dẫn chi tiết để thiết lập và chạy dự án Quick Commerce.

---

## 📋 Mục Lục

- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Quick Start](#quick-start)
- [Phase 1: Database](#phase-1-database)
- [Phase 2: Backend API](#phase-2-backend-api)
- [API Usage](#api-usage)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ Yêu Cầu Hệ Thống

| Phần mềm | Version | Bắt buộc |
|----------|---------|----------|
| Docker Desktop | 4.0+ | ✅ |
| Git | 2.0+ | ✅ |
| Python | 3.11+ | Chỉ cho development |

---

## 🚀 Quick Start

```powershell
# 1. Clone project
git clone <repo-url>
cd Web_Shop

# 2. Start all services
docker-compose up -d

# 3. Wait 30s for initialization...

# 4. Access
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs
# Adminer: http://localhost:8080
```

---

## 🗄️ Phase 1: Database

### Services
- **PostgreSQL**: Port 5433
- **Adminer**: Port 8080

### Access Database

```powershell
# Via Adminer
# URL: http://localhost:8080
# System: PostgreSQL
# Server: postgres
# User: shop_user
# Password: shop_password_123
# Database: shop_db

# Via CLI
docker exec -it shop_db psql -U shop_user -d shop_db
```

### Mock Data
- 6 Users (2 admin, 2 staff, 2 customers)
- 10 Categories
- 78 Products
- 100+ Inventory Batches
- 5 Sample Orders

### Download Product Images

```powershell
# Install Python dependencies
pip install -r requirements.txt

# Download images
python scripts/download_images.py
```

---

## ⚡ Phase 2: Backend API

### Services
- **Backend (FastAPI)**: Port 8000
- **Redis**: Port 6379

### API Documentation

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Health check |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

### Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@shop.vn | password123 | Admin |
| staff1@shop.vn | password123 | Staff |
| khach1@gmail.com | password123 | Customer |

### Key Features

1. **JWT Authentication**
   - Access token: 30 minutes
   - Refresh token: 7 days

2. **Role-based Access**
   - Customer: Cart, Orders
   - Staff: + Products, Categories
   - Admin: + Users, Inventory

3. **FEFO Inventory**
   - First Expired First Out
   - Pessimistic Locking (no race conditions)

4. **Alembic Migrations**
   - Auto-run on container start

---

## 📝 API Usage

### 1. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "khach1@gmail.com", "password": "password123"}'
```

Response:
```json
{
  "user": {"id": 5, "email": "khach1@gmail.com", ...},
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  }
}
```

### 2. Get Products

```bash
curl http://localhost:8000/api/v1/products
```

### 3. Add to Cart (Authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/cart/items \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### 4. Create Order

```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_address": "123 Nguyen Hue, Q1, TPHCM",
    "customer_phone": "0901234567",
    "customer_name": "Test Customer",
    "payment_method": "cod"
  }'
```

---

## 🔧 Commands

### Docker

```powershell
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild (after code changes)
docker-compose up -d --build

# Logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

### Alembic Migrations

```powershell
# Auto-generate migration
docker exec -it shop_backend alembic revision --autogenerate -m "description"

# Apply migrations
docker exec -it shop_backend alembic upgrade head

# Rollback
docker exec -it shop_backend alembic downgrade -1

# History
docker exec -it shop_backend alembic history
```

### Testing

```powershell
# Run tests
docker exec -it shop_backend pytest tests/ -v

# Specific test
docker exec -it shop_backend pytest tests/test_auth.py -v
```

---

## 🔧 Troubleshooting

### Port Already in Use

```powershell
# Find process using port
netstat -ano | findstr :5433
netstat -ano | findstr :8000

# Change port in .env or docker-compose.yml
```

### Docker Not Running

1. Open Docker Desktop
2. Wait for it to start
3. Retry `docker-compose up -d`

### Backend Not Starting

```powershell
# Check logs
docker-compose logs backend

# Common issues:
# - Database not ready: Wait 30s
# - Import error: Check Python syntax
```

### Database Connection Failed

```powershell
# Check PostgreSQL
docker-compose ps
docker-compose logs postgres

# Reset if needed
docker-compose down -v
docker-compose up -d
```

---

## ✅ Checklist

### Phase 1
- [ ] Docker Desktop installed
- [ ] `docker-compose up -d` successful
- [ ] Adminer accessible at :8080
- [ ] Mock data loaded

### Phase 2
- [ ] Backend running at :8000
- [ ] Swagger UI accessible at :8000/docs
- [ ] Login working
- [ ] Create order working

---

## 🚀 Next: Phase 3 (Frontend)

- React.js with Vite
- Customer Portal
- Staff Dashboard
- Admin Panel

---

📧 **Need help?** Create an issue or contact instructor.
