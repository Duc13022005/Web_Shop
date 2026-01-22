# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG

Hướng dẫn chi tiết từng bước để thiết lập và chạy Phase 1 của dự án Cửa Hàng Tiện Lợi.

## 📋 Mục Lục

- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Bước 1: Cài Đặt Môi Trường](#bước-1-cài-đặt-môi-trường)
- [Bước 2: Khởi Động Database](#bước-2-khởi-động-database)
- [Bước 3: Cài Đặt Python Dependencies](#bước-3-cài-đặt-python-dependencies)
- [Bước 4: Tải Ảnh Sản Phẩm](#bước-4-tải-ảnh-sản-phẩm)
- [Bước 5: Kiểm Tra Database](#bước-5-kiểm-tra-database)
- [Bước 6: Xem Kết Quả](#bước-6-xem-kết-quả)
- [Troubleshooting](#troubleshooting)
- [Các Lệnh Hữu Ích](#các-lệnh-hữu-ích)

---

## 🖥️ Yêu Cầu Hệ Thống

### Phần mềm bắt buộc

| Phần mềm | Version | Link Download |
|----------|---------|---------------|
| **Docker Desktop** | 4.0+ | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| **Python** | 3.10+ | [python.org/downloads](https://www.python.org/downloads/) |
| **Git** | 2.0+ | [git-scm.com](https://git-scm.com/) |

### Kiểm tra cài đặt

```powershell
# Kiểm tra Docker
docker --version
# Output: Docker version 24.x.x

# Kiểm tra Python
python --version
# Output: Python 3.10.x

# Kiểm tra Git
git --version
# Output: git version 2.x.x
```

### Yêu cầu phần cứng

- RAM: Tối thiểu 4GB (khuyến nghị 8GB)
- Disk: Tối thiểu 2GB trống
- Internet: Cần để tải Docker images và ảnh sản phẩm

---

## 📥 Bước 1: Cài Đặt Môi Trường

### 1.1. Clone hoặc tải project

```powershell
# Nếu dùng Git
git clone <repository-url>
cd Web_Shop

# Hoặc download ZIP và giải nén
```

### 1.2. Tạo file .env

File `.env` đã được tạo sẵn, nhưng bạn có thể tùy chỉnh:

```powershell
# Copy từ template (nếu cần)
copy .env.example .env

# Mở và chỉnh sửa nếu muốn đổi password
notepad .env
```

**Nội dung .env:**
```ini
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=shop_db
POSTGRES_USER=shop_user
POSTGRES_PASSWORD=shop_password_123
```

> ⚠️ **Lưu ý**: Trong production, hãy đổi password mạnh hơn!

---

## 🐘 Bước 2: Khởi Động Database

### 2.1. Đảm bảo Docker Desktop đang chạy

Mở Docker Desktop và đợi nó khởi động hoàn tất.

### 2.2. Khởi động PostgreSQL

```powershell
# Di chuyển đến thư mục project
cd d:\DNU\Web_Shop

# Khởi động containers
docker-compose up -d
```

**Output mong đợi:**
```
[+] Running 3/3
 ✔ Network web_shop_shop_network  Created
 ✔ Container shop_db              Started
 ✔ Container shop_adminer         Started
```

### 2.3. Kiểm tra containers đang chạy

```powershell
docker-compose ps
```

**Output mong đợi:**
```
NAME            STATUS                   PORTS
shop_adminer    Up                       0.0.0.0:8080->8080/tcp
shop_db         Up (healthy)             0.0.0.0:5432->5432/tcp
```

### 2.4. Đợi database khởi tạo

Lần đầu chạy, Docker sẽ:
1. Tải PostgreSQL image (~150MB)
2. Tạo database `shop_db`
3. Chạy `init.sql` (tạo tables)
4. Chạy `mock_data.sql` (insert data)

Xem logs để theo dõi:
```powershell
docker-compose logs -f postgres
```

Đợi đến khi thấy:
```
LOG:  database system is ready to accept connections
```

Nhấn `Ctrl+C` để thoát logs.

---

## 🐍 Bước 3: Cài Đặt Python Dependencies

### 3.1. Tạo Virtual Environment (khuyến nghị)

```powershell
# Tạo venv
python -m venv venv

# Kích hoạt venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Hoặc Command Prompt
.\venv\Scripts\activate.bat
```

### 3.2. Cài đặt packages

```powershell
pip install -r requirements.txt
```

**Packages sẽ được cài:**
- `psycopg2-binary` - PostgreSQL driver
- `bing-image-downloader` - Tải ảnh từ Bing
- `python-dotenv` - Đọc file .env
- `requests` - HTTP client
- `Pillow` - Xử lý ảnh
- `tabulate` - Hiển thị bảng trong terminal

---

## 🖼️ Bước 4: Tải Ảnh Sản Phẩm

### 4.1. Xem danh sách categories

```powershell
python scripts/download_images.py --list
```

**Output:**
```
📋 Danh sách categories:
   - do-uong: 15 sản phẩm
   - banh-keo: 10 sản phẩm
   - mi-an-lien: 8 sản phẩm
   ...
```

### 4.2. Chạy dry-run trước (tùy chọn)

```powershell
python scripts/download_images.py --dry-run
```

### 4.3. Tải ảnh

```powershell
# Tải tất cả categories
python scripts/download_images.py

# Hoặc tải từng category
python scripts/download_images.py --category do-uong
python scripts/download_images.py --category banh-keo
```

> ⏱️ **Thời gian**: Khoảng 5-15 phút tùy tốc độ mạng

**Cấu trúc sau khi tải:**
```
src/uploads/
├── do-uong/
│   ├── DRINK001.jpg
│   ├── DRINK002.jpg
│   └── ...
├── banh-keo/
│   ├── SNACK001.jpg
│   └── ...
└── ...
```

### 4.4. Xử lý nếu tải lỗi

Nếu Bing không trả về ảnh, script sẽ tự động tạo placeholder. Bạn có thể:

1. **Thử lại**: `python scripts/download_images.py --category <tên>`
2. **Tải manual**: Tìm ảnh và đặt vào thư mục với đúng tên SKU
3. **Dọn dẹp temp**: `python scripts/download_images.py --cleanup`

---

## ✅ Bước 5: Kiểm Tra Database

### 5.1. Chạy test connection

```powershell
python scripts/test_connection.py
```

**Output mong đợi:**
```
============================================================
🔗 KIỂM TRA KẾT NỐI DATABASE
============================================================

📡 Config:
   Host: localhost
   Port: 5432
   Database: shop_db
   User: shop_user

✅ Kết nối thành công!
   PostgreSQL: PostgreSQL 16.x

============================================================
📊 TỔNG QUAN DATABASE
============================================================

📋 Số lượng records:
Table               Records
----------------  ---------
Users                     6
Categories               10
Products                 78
Inventory Batches       100
Orders                    5
...
```

### 5.2. Xem chi tiết từng phần

```powershell
# Chỉ xem users
python scripts/test_connection.py --users

# Chỉ xem sản phẩm
python scripts/test_connection.py --products

# Chỉ xem tồn kho (FEFO)
python scripts/test_connection.py --inventory

# Kiểm tra ảnh
python scripts/test_connection.py --images
```

---

## 👀 Bước 6: Xem Kết Quả

### 6.1. Adminer (Database UI)

Mở trình duyệt và truy cập:
```
http://localhost:8080
```

**Thông tin đăng nhập:**
- System: PostgreSQL
- Server: postgres (hoặc shop_db)
- Username: shop_user
- Password: shop_password_123
- Database: shop_db

### 6.2. Test Display HTML

Mở file HTML trong trình duyệt:
```powershell
# Mở bằng trình duyệt mặc định
start scripts\test_display.html
```

Trang web sẽ hiển thị:
- Thống kê tổng quan
- Danh sách sản phẩm theo category
- Ảnh sản phẩm (nếu đã tải)

### 6.3. Truy vấn SQL trực tiếp

```powershell
# Vào PostgreSQL shell
docker exec -it shop_db psql -U shop_user -d shop_db

# Một số query mẫu:
SELECT * FROM categories;
SELECT * FROM products LIMIT 10;
SELECT * FROM v_products_with_stock LIMIT 10;

# Thoát
\q
```

---

## 🔧 Troubleshooting

### Lỗi: Port 5432 đã được sử dụng

```powershell
# Tìm process đang dùng port
netstat -ano | findstr :5432

# Đổi port trong .env
POSTGRES_PORT=5433

# Restart
docker-compose down
docker-compose up -d
```

### Lỗi: Docker không chạy

1. Mở Docker Desktop
2. Đợi Docker khởi động (icon ở taskbar chuyển xanh)
3. Thử lại `docker-compose up -d`

### Lỗi: Permission denied khi chạy PowerShell script

```powershell
# Cho phép chạy scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi: psycopg2 không cài được

```powershell
# Cài binary version
pip install psycopg2-binary

# Nếu vẫn lỗi, cài build tools
# Download từ: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Lỗi: bing-image-downloader không hoạt động

Script sẽ tự động tạo placeholder. Hoặc:
```powershell
# Cập nhật package
pip install --upgrade bing-image-downloader

# Nếu vẫn lỗi, tải ảnh manual và đặt vào src/uploads/{category}/{SKU}.jpg
```

### Reset database hoàn toàn

```powershell
# Dừng và xóa volume
docker-compose down -v

# Khởi động lại (sẽ chạy lại init.sql và mock_data.sql)
docker-compose up -d
```

---

## 📝 Các Lệnh Hữu Ích

### Docker

```powershell
# Khởi động
docker-compose up -d

# Dừng
docker-compose down

# Xem logs
docker-compose logs -f

# Restart
docker-compose restart

# Xem status
docker-compose ps

# Vào shell container
docker exec -it shop_db bash

# Vào PostgreSQL
docker exec -it shop_db psql -U shop_user -d shop_db
```

### Python Scripts

```powershell
# Test connection - tất cả
python scripts/test_connection.py

# Test connection - chỉ summary
python scripts/test_connection.py --summary

# Download images - dry run
python scripts/download_images.py --dry-run

# Download images - một category
python scripts/download_images.py -c do-uong

# Download images - tất cả
python scripts/download_images.py
```

### PostgreSQL CLI

```sql
-- Liệt kê tables
\dt

-- Mô tả table
\d products

-- Xem categories với số sản phẩm
SELECT c.name, COUNT(p.id) 
FROM categories c 
LEFT JOIN products p ON c.id = p.category_id 
GROUP BY c.name;

-- Xem sản phẩm sắp hết hạn
SELECT p.name, ib.expiry_date, ib.quantity_on_hand 
FROM inventory_batches ib 
JOIN products p ON ib.product_id = p.id 
WHERE ib.expiry_date < CURRENT_DATE + INTERVAL '30 days'
ORDER BY ib.expiry_date;

-- Xem view products với stock
SELECT * FROM v_products_with_stock LIMIT 10;
```

---

## ✅ Checklist Hoàn Thành Phase 1

- [ ] Docker Desktop đã cài đặt và chạy
- [ ] `docker-compose up -d` thành công
- [ ] `pip install -r requirements.txt` thành công
- [ ] `python scripts/test_connection.py` hiển thị data
- [ ] `python scripts/download_images.py` hoàn thành
- [ ] Adminer có thể truy cập tại `localhost:8080`
- [ ] `test_display.html` hiển thị sản phẩm với ảnh

---

## 🚀 Tiếp Theo: Phase 2

Sau khi hoàn thành Phase 1, chuyển sang Phase 2 để xây dựng Backend API với FastAPI:

- Tạo project structure
- Implement Authentication (JWT)
- Xây dựng CRUD APIs
- Implement Business Logic (Orders, Inventory FEFO)
- Unit Testing

---

📧 **Cần hỗ trợ?** Tạo issue trên repository hoặc liên hệ giảng viên.
