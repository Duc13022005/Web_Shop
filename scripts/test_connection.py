"""
Database Connection Test Script - Cửa Hàng Tiện Lợi
Kiểm tra kết nối và hiển thị data từ PostgreSQL

Usage:
    python scripts/test_connection.py              # Chạy tất cả tests
    python scripts/test_connection.py --summary    # Chỉ hiển thị tổng quan
    python scripts/test_connection.py --products   # Hiển thị sản phẩm
    python scripts/test_connection.py --inventory  # Hiển thị tồn kho
"""

import os
import sys
from pathlib import Path
from datetime import date
from tabulate import tabulate

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("❌ psycopg2 chưa được cài đặt. Chạy: pip install psycopg2-binary")
    sys.exit(1)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "database": os.getenv("POSTGRES_DB", "shop_db"),
    "user": os.getenv("POSTGRES_USER", "shop_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "shop_password_123"),
}

# Paths
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "src" / "uploads"


def get_connection():
    """Tạo kết nối đến database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Không thể kết nối database: {e}")
        return None


def test_connection():
    """Test kết nối cơ bản"""
    print("\n" + "=" * 60)
    print("🔗 KIỂM TRA KẾT NỐI DATABASE")
    print("=" * 60)
    
    print(f"\n📡 Config:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Port: {DB_CONFIG['port']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print(f"   User: {DB_CONFIG['user']}")
    
    conn = get_connection()
    if conn:
        print("\n✅ Kết nối thành công!")
        
        # Get PostgreSQL version
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"   PostgreSQL: {version.split(',')[0]}")
        
        conn.close()
        return True
    return False


def get_table_counts():
    """Đếm số records trong mỗi table"""
    conn = get_connection()
    if not conn:
        return None
    
    tables = ["users", "categories", "products", "inventory_batches", "orders", "order_items", "carts", "cart_items"]
    counts = {}
    
    with conn.cursor() as cur:
        for table in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                counts[table] = cur.fetchone()[0]
            except:
                counts[table] = "N/A"
    
    conn.close()
    return counts


def display_summary():
    """Hiển thị tổng quan database"""
    print("\n" + "=" * 60)
    print("📊 TỔNG QUAN DATABASE")
    print("=" * 60)
    
    counts = get_table_counts()
    if not counts:
        return
    
    print("\n📋 Số lượng records:")
    data = [[table.title().replace("_", " "), count] for table, count in counts.items()]
    print(tabulate(data, headers=["Table", "Records"], tablefmt="simple"))


def display_users():
    """Hiển thị danh sách users"""
    print("\n" + "=" * 60)
    print("👥 DANH SÁCH USERS")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, email, full_name, phone, role, is_active
            FROM users
            ORDER BY role, id;
        """)
        users = cur.fetchall()
    
    conn.close()
    
    if users:
        data = [[u['id'], u['email'], u['full_name'], u['role'], '✓' if u['is_active'] else '✗'] 
                for u in users]
        print(tabulate(data, headers=["ID", "Email", "Họ tên", "Vai trò", "Active"], tablefmt="simple"))
    else:
        print("   Không có dữ liệu")


def display_categories():
    """Hiển thị danh sách categories"""
    print("\n" + "=" * 60)
    print("📁 DANH SÁCH DANH MỤC")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT c.id, c.name, c.slug, COUNT(p.id) as product_count
            FROM categories c
            LEFT JOIN products p ON c.id = p.category_id
            GROUP BY c.id, c.name, c.slug
            ORDER BY c.sort_order;
        """)
        categories = cur.fetchall()
    
    conn.close()
    
    if categories:
        data = [[c['id'], c['name'], c['slug'], c['product_count']] for c in categories]
        print(tabulate(data, headers=["ID", "Tên", "Slug", "Số SP"], tablefmt="simple"))
    else:
        print("   Không có dữ liệu")


def display_products(limit: int = 20):
    """Hiển thị danh sách sản phẩm"""
    print("\n" + "=" * 60)
    print(f"🛒 DANH SÁCH SẢN PHẨM (Top {limit})")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                p.id, p.sku, p.name, c.name as category,
                p.base_price, p.sale_price, p.unit,
                p.is_age_restricted
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.category_id, p.id
            LIMIT %s;
        """, (limit,))
        products = cur.fetchall()
    
    conn.close()
    
    if products:
        data = []
        for p in products:
            price = p['sale_price'] or p['base_price']
            age = "18+" if p['is_age_restricted'] else ""
            data.append([p['sku'], p['name'][:25], p['category'][:15], f"{price:,.0f}đ", p['unit'], age])
        
        print(tabulate(data, headers=["SKU", "Tên SP", "Danh mục", "Giá", "ĐVT", "18+"], tablefmt="simple"))
    else:
        print("   Không có dữ liệu")


def display_inventory():
    """Hiển thị tồn kho theo FEFO (First Expired First Out)"""
    print("\n" + "=" * 60)
    print("📦 TỒN KHO (FEFO - Sắp hết hạn trước)")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                p.sku, p.name, ib.batch_code, 
                ib.expiry_date, ib.quantity_on_hand,
                ib.quantity_reserved, ib.location
            FROM inventory_batches ib
            JOIN products p ON ib.product_id = p.id
            WHERE ib.expiry_date IS NOT NULL
            ORDER BY ib.expiry_date ASC
            LIMIT 20;
        """)
        batches = cur.fetchall()
    
    conn.close()
    
    if batches:
        today = date.today()
        data = []
        for b in batches:
            days_left = (b['expiry_date'] - today).days
            status = "⚠️" if days_left < 30 else ("🔴" if days_left < 7 else "✓")
            available = b['quantity_on_hand'] - b['quantity_reserved']
            data.append([
                b['sku'], 
                b['name'][:20], 
                b['batch_code'][-8:],
                str(b['expiry_date']),
                f"{days_left}d",
                available,
                b['location'][:10],
                status
            ])
        
        print(tabulate(data, 
                      headers=["SKU", "Tên SP", "Lô", "HSD", "Còn", "SL", "Vị trí", ""], 
                      tablefmt="simple"))
    else:
        print("   Không có dữ liệu")


def display_orders():
    """Hiển thị đơn hàng gần đây"""
    print("\n" + "=" * 60)
    print("🧾 ĐƠN HÀNG GẦN ĐÂY")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                o.id, o.customer_name, o.status, 
                o.total_amount, o.payment_method, o.payment_status,
                o.created_at
            FROM orders o
            ORDER BY o.created_at DESC
            LIMIT 10;
        """)
        orders = cur.fetchall()
    
    conn.close()
    
    if orders:
        status_map = {
            'pending': '⏳ Chờ',
            'confirmed': '✓ Xác nhận',
            'picking': '📦 Soạn',
            'delivering': '🚚 Giao',
            'completed': '✅ Xong',
            'cancelled': '❌ Hủy'
        }
        
        data = []
        for o in orders:
            status = status_map.get(o['status'], o['status'])
            data.append([
                o['id'],
                o['customer_name'][:15],
                status,
                f"{o['total_amount']:,.0f}đ",
                o['payment_method'].upper(),
                o['payment_status']
            ])
        
        print(tabulate(data, 
                      headers=["ID", "Khách hàng", "Trạng thái", "Tổng tiền", "TT", "Thanh toán"], 
                      tablefmt="simple"))
    else:
        print("   Không có dữ liệu")


def check_images():
    """Kiểm tra ảnh sản phẩm đã tải"""
    print("\n" + "=" * 60)
    print("🖼️ KIỂM TRA ẢNH SẢN PHẨM")
    print("=" * 60)
    
    conn = get_connection()
    if not conn:
        return
    
    # Get all products with their category slugs
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT p.sku, p.name, c.slug as category_slug
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY p.category_id, p.id;
        """)
        products = cur.fetchall()
    
    conn.close()
    
    if not UPLOADS_DIR.exists():
        print(f"   ⚠️  Thư mục uploads chưa tồn tại: {UPLOADS_DIR}")
        return
    
    # Check each category
    categories = {}
    for p in products:
        cat = p['category_slug']
        if cat not in categories:
            categories[cat] = {"total": 0, "found": 0, "missing": []}
        
        categories[cat]["total"] += 1
        
        image_path = UPLOADS_DIR / cat / f"{p['sku']}.jpg"
        if image_path.exists():
            categories[cat]["found"] += 1
        else:
            categories[cat]["missing"].append(p['sku'])
    
    # Display summary
    data = []
    for cat, info in categories.items():
        status = "✅" if info["found"] == info["total"] else "⚠️"
        data.append([cat, info["found"], info["total"], status])
    
    print(tabulate(data, headers=["Category", "Có ảnh", "Tổng SP", ""], tablefmt="simple"))
    
    # Show missing files
    print("\n🔍 Ảnh thiếu:")
    total_missing = 0
    for cat, info in categories.items():
        if info["missing"]:
            total_missing += len(info["missing"])
            print(f"   {cat}: {', '.join(info['missing'][:5])}{'...' if len(info['missing']) > 5 else ''}")
    
    if total_missing == 0:
        print("   ✅ Tất cả sản phẩm đều có ảnh!")


def run_all_tests():
    """Chạy tất cả tests"""
    if not test_connection():
        return
    
    display_summary()
    display_users()
    display_categories()
    display_products()
    display_inventory()
    display_orders()
    check_images()
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH KIỂM TRA!")
    print("=" * 60)


def main():
    import argparse
    
    # Check tabulate
    try:
        from tabulate import tabulate
    except ImportError:
        print("⚠️  tabulate chưa được cài. Chạy: pip install tabulate")
        # Simple fallback
        global tabulate
        tabulate = lambda data, headers, tablefmt: "\n".join([str(h) for h in headers] + [str(r) for r in data])
    
    parser = argparse.ArgumentParser(description="Test database connection và hiển thị data")
    parser.add_argument("--summary", "-s", action="store_true", help="Chỉ hiển thị tổng quan")
    parser.add_argument("--users", "-u", action="store_true", help="Hiển thị users")
    parser.add_argument("--categories", "-c", action="store_true", help="Hiển thị categories")
    parser.add_argument("--products", "-p", action="store_true", help="Hiển thị products")
    parser.add_argument("--inventory", "-i", action="store_true", help="Hiển thị inventory")
    parser.add_argument("--orders", "-o", action="store_true", help="Hiển thị orders")
    parser.add_argument("--images", action="store_true", help="Kiểm tra ảnh sản phẩm")
    
    args = parser.parse_args()
    
    # If no specific flag, run all
    if not any([args.summary, args.users, args.categories, args.products, 
                args.inventory, args.orders, args.images]):
        run_all_tests()
        return
    
    # Run specific tests
    if not test_connection():
        return
    
    if args.summary:
        display_summary()
    if args.users:
        display_users()
    if args.categories:
        display_categories()
    if args.products:
        display_products()
    if args.inventory:
        display_inventory()
    if args.orders:
        display_orders()
    if args.images:
        check_images()


if __name__ == "__main__":
    main()
