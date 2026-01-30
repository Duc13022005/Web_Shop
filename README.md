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

## 🚀 Hướng Dẫn Chạy (Đơn Giản Nhất)

Bạn chỉ cần làm theo 3 bước sau là chạy được ngay website:

### Bước 1: Cài đặt phần mềm
- Tải và cài đặt **Docker Desktop** tại đây: [Download Docker](https://www.docker.com/products/docker-desktop/)
- Sau khi cài xong, hãy **mở Docker Desktop lên** và chờ nó khởi động (có icon cá voi màu xanh ở góc màn hình).

### Bước 2: Tải và chạy Code
1. Tải code này về máy tính (nếu tải file Zip thì hãy giải nén ra).
2. Vào thư mục chứa code (thư mục `Web_Shop`).
3. Tìm file `.env.example`, copy và đổi tên thành `.env` (nếu chưa có).
4. Chuột phải vào khoảng trắng trong thư mục, chọn **"Open Terminal Here"** (hoặc mở CMD/PowerShell).
5. Gõ lệnh sau rồi ấn Enter:
   ```powershell
   docker-compose up -d
   ```
   *(Lệnh này sẽ tự động tải mọi thứ cần thiết về, bạn chỉ cần chờ khoảng 5-10 phút cho lần đầu tiên)*.

### Bước 3: Truy cập Website
Sau khi chạy xong, hãy mở trình duyệt và trải nghiệm:

- **Trang web bán hàng**: [http://localhost](http://localhost)
- **Tài liệu API (Cho Dev)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Quản lý Database**: [http://localhost:8080](http://localhost:8080)
  - Hệ thống: `PostgreSQL`
  - Server: `db`
  - User: `shop_user`
  - Password: `shop_password_123`
  - Database: `shop_db`

### Tài khoản đăng nhập mẫu
| Vai trò | Email | Mật khẩu | Mô tả |
|---|---|---|---|
| Admin | `admin@shop.vn` | `password123` | Quản trị viên cao nhất |
| Staff | `staff1@shop.vn` | `password123` | Nhân viên quản lý đơn hàng |
| Customer | `khach1@gmail.com` | `password123` | Khách hàng mua sắm |

**Lưu ý:** Để tắt website, hãy gõ lệnh: `docker-compose down`

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

## 📦 Hướng Dẫn Nâng Cao (Data & Images)

### 1. Đồng bộ Dữ Liệu (Database)
Nếu bạn muốn export dữ liệu hiện tại hoặc import dữ liệu từ máy khác:

**Cách 1: Sử dụng Script (Khuyên dùng)**
- **Export Data**: Chạy file `scripts/export_db.ps1` (Dữ liệu sẽ được lưu vào `src/db/dump.sql`)
- **Import Data**: Chạy file `scripts/import_db.ps1` (Sẽ import từ `src/db/dump.sql` vào database)

**Cách 2: Chạy lệnh thủ công**
- Export: `docker exec db pg_dump -U shop_user -d shop_db --data-only --column-inserts > src/db/dump.sql`
- Import: `cat src/db/dump.sql | docker exec -i db psql -U shop_user -d shop_db`


### 2. Cập nhật Hình Ảnh Sản Phẩm
Vì ảnh sản phẩm không được lưu trên Git, bạn cần tải thủ công bộ ảnh chuẩn:

1. **Tải ảnh**: Truy cập [Google Drive Folder](https://drive.google.com/drive/folders/1KKtFYXZQZdfCZYVtMwJn_6NbCmOg6NeP?usp=sharing)
2. **Giải nén/Copy**:
   - Copy toàn bộ các file ảnh vào thư mục: `src/backend/uploads/`
   - *Lưu ý*: Nếu thư mục `src/backend/uploads/` chưa có, hãy tạo mới nó.
   - Cấu trúc đúng sẽ là: `src/backend/uploads/product_1.jpg`, v.v...
3. **Kiểm tra**:
   - Truy cập lại website, ảnh sản phẩm sẽ hiển thị bình thường.


---

Made with ❤️ for DNU Web Development Course
