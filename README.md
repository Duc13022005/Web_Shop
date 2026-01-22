# 🏪 Quick Commerce - Cửa Hàng Tiện Lợi

Dự án website cửa hàng tiện lợi với mô hình Quick Commerce, hỗ trợ đặt hàng online, quản lý kho hàng, và bán hàng đa kênh.

![Version](https://img.shields.io/badge/version-1.0.0--phase1-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Mục Lục

- [Tổng Quan](#tổng-quan)
- [Tính Năng](#tính-năng)
- [Tech Stack](#tech-stack)
- [Cấu Trúc Project](#cấu-trúc-project)
- [Cài Đặt](#cài-đặt)
- [Sử Dụng](#sử-dụng)
- [Database Schema](#database-schema)
- [Phases Phát Triển](#phases-phát-triển)

## 🎯 Tổng Quan

Hệ thống Quick Commerce cho cửa hàng tiện lợi, phục vụ:

| Vai trò | Chức năng |
|---------|-----------|
| **Khách hàng** | Đặt hàng online, theo dõi đơn hàng, thanh toán |
| **Nhân viên (Staff)** | Quản lý mặt hàng, xử lý đơn hàng, bán hàng POS |
| **Quản trị (Admin)** | Quản lý kho, quản lý người dùng, báo cáo |

### Đặc thù Quick Commerce

- ⚡ **Giao hàng nhanh** - Dưới 30-60 phút
- 📦 **Quản lý lô hàng (FEFO)** - First Expired First Out
- 🔄 **Real-time Inventory** - Cập nhật tồn kho tức thì
- 🔞 **Age Verification** - Kiểm soát sản phẩm hạn chế độ tuổi

## ✨ Tính Năng

### Phase 1 (Hiện tại) ✅
- [x] Database PostgreSQL với Docker
- [x] Schema thiết kế theo FEFO
- [x] Mock data tiếng Việt (78 sản phẩm, 10 danh mục)
- [x] Script cào ảnh sản phẩm
- [x] Test connection và display

### Phase 2 (Sắp tới)
- [ ] FastAPI Backend
- [ ] RESTful API
- [ ] JWT Authentication
- [ ] Business Logic (Orders, Inventory)

### Phase 3
- [ ] React Frontend
- [ ] Customer Portal
- [ ] Staff Dashboard
- [ ] Admin Panel

### Phase 4
- [ ] Integration Testing
- [ ] Cloud Deployment

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Database** | PostgreSQL 16 (Docker) |
| **Backend** | Python 3.10+, FastAPI (Phase 2) |
| **Frontend** | React, Vite (Phase 3) |
| **Containerization** | Docker, Docker Compose |
| **Other** | Redis (caching), Adminer (DB UI) |

## 📁 Cấu Trúc Project

```
Web_Shop/
├── 📄 docker-compose.yml      # Docker services configuration
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env                    # Environment variables (local)
├── 📄 .env.example           # Environment template
├── 📄 .gitignore
├── 📄 README.md              # This file
├── 📄 GUIDE.md               # Detailed setup guide
│
├── 📁 database/
│   ├── 📄 init.sql           # Database schema
│   └── 📄 mock_data.sql      # Vietnamese mock data
│
├── 📁 scripts/
│   ├── 📄 download_images.py  # Image downloader
│   ├── 📄 test_connection.py  # Database test
│   └── 📄 test_display.html   # Visual test page
│
└── 📁 src/
    └── 📁 uploads/            # Product images
        ├── 📁 do-uong/
        ├── 📁 banh-keo/
        └── ...
```

## 🚀 Cài Đặt

### Yêu Cầu

- Docker Desktop
- Python 3.10+
- Git

### Quick Start

```powershell
# 1. Clone repository
git clone <repo-url>
cd Web_Shop

# 2. Start PostgreSQL
docker-compose up -d

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Download product images
python scripts/download_images.py

# 5. Test database connection
python scripts/test_connection.py
```

> 📖 Xem chi tiết tại [GUIDE.md](./GUIDE.md)

## 💾 Database Schema

### ERD Overview

```
users ──────────┬──────────── orders
                │                │
                │                ├── order_items
                │                │       │
categories ─── products ────────┴─── inventory_batches
                │
                └── cart_items ── carts
```

### Key Tables

| Table | Mô tả | Records |
|-------|-------|---------|
| `users` | Người dùng (customer, staff, admin) | 6 |
| `categories` | Danh mục sản phẩm | 10 |
| `products` | Sản phẩm | 78 |
| `inventory_batches` | Lô hàng (FEFO) | 100+ |
| `orders` | Đơn hàng | 5 (sample) |

### Test Accounts

| Email | Password | Role |
|-------|----------|------|
| admin@shop.vn | password123 | Admin |
| staff1@shop.vn | password123 | Staff |
| khach1@gmail.com | password123 | Customer |

## 📊 Mock Data

### Danh mục sản phẩm

1. 🥤 Đồ uống (15 sản phẩm)
2. 🍪 Bánh kẹo (10 sản phẩm)
3. 🍜 Mì & Thực phẩm ăn liền (8 sản phẩm)
4. 🥛 Sữa & Sản phẩm từ sữa (8 sản phẩm)
5. 🧊 Đồ đông lạnh (6 sản phẩm)
6. 🧂 Gia vị & Nước chấm (8 sản phẩm)
7. 🧴 Chăm sóc cá nhân (8 sản phẩm)
8. 🧹 Đồ gia dụng (6 sản phẩm)
9. 🍺 Rượu bia (5 sản phẩm) - **18+**
10. 🚬 Thuốc lá (4 sản phẩm) - **18+**

### FEFO (First Expired First Out)

Mỗi sản phẩm có thể có nhiều lô hàng với:
- `batch_code`: Mã lô
- `expiry_date`: Ngày hết hạn (sort để xuất trước)
- `quantity_on_hand`: Số lượng thực tế
- `quantity_reserved`: Số lượng đã giữ chỗ
- `location`: Vị trí trong kho

## 🔧 Commands

```powershell
# Start database
docker-compose up -d

# Stop database
docker-compose down

# View logs
docker-compose logs -f postgres

# Access database shell
docker exec -it shop_db psql -U shop_user -d shop_db

# Reset database (delete + recreate)
docker-compose down -v
docker-compose up -d
```

## 📚 Documentation

- [GUIDE.md](./GUIDE.md) - Hướng dẫn chi tiết từng bước
- [database/init.sql](./database/init.sql) - Database schema
- [database/mock_data.sql](./database/mock_data.sql) - Mock data

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License.

---

Made with ❤️ for DNU Web Development Course
