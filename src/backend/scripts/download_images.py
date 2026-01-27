"""
Image Downloader Script - Cửa Hàng Tiện Lợi
Tải ảnh sản phẩm từ Bing Image Search và lưu vào src/uploads/{category}/

Usage:
    python scripts/download_images.py              # Download tất cả
    python scripts/download_images.py --category do-uong  # Download theo category
    python scripts/download_images.py --dry-run    # Chỉ hiển thị, không tải
"""

import os
import sys
import time
import argparse
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from bing_image_downloader import downloader
    BING_AVAILABLE = True
except ImportError:
    BING_AVAILABLE = False
    print("⚠️  bing-image-downloader chưa được cài đặt. Sẽ sử dụng placeholder images.")

try:
    import requests
    from PIL import Image
    from io import BytesIO
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
TEMP_DIR = BASE_DIR / "temp_images"

# Số ảnh tải cho mỗi sản phẩm
IMAGES_PER_PRODUCT = int(os.getenv("IMAGES_PER_PRODUCT", "1"))

# Product data - mapping từ mock_data.sql
PRODUCTS_BY_CATEGORY = {
    "do-uong": [
        {"sku": "DRINK001", "name": "Coca-Cola", "search": "coca cola can 330ml"},
        {"sku": "DRINK002", "name": "Pepsi", "search": "pepsi can 330ml"},
        {"sku": "DRINK003", "name": "Trà xanh 0 độ", "search": "tra xanh 0 do chai"},
        {"sku": "DRINK004", "name": "Lavie", "search": "lavie water bottle vietnam"},
        {"sku": "DRINK005", "name": "Teppy", "search": "teppy orange juice vietnam"},
        {"sku": "DRINK006", "name": "Highlands Coffee", "search": "highlands coffee can vietnam"},
        {"sku": "DRINK007", "name": "Red Bull", "search": "red bull energy drink can"},
        {"sku": "DRINK008", "name": "Sting", "search": "sting energy drink vietnam"},
        {"sku": "DRINK009", "name": "Fuze Tea", "search": "fuze tea peach bottle"},
        {"sku": "DRINK010", "name": "Cocoxim", "search": "cocoxim coconut water"},
        {"sku": "DRINK011", "name": "Aquafina", "search": "aquafina water bottle"},
        {"sku": "DRINK012", "name": "C2", "search": "c2 green tea vietnam"},
        {"sku": "DRINK013", "name": "Nước yến Sante", "search": "nuoc yen sante vietnam"},
        {"sku": "DRINK014", "name": "Revive", "search": "revive isotonic drink vietnam"},
        {"sku": "DRINK015", "name": "Fanta", "search": "fanta orange can 330ml"},
    ],
    "banh-keo": [
        {"sku": "SNACK001", "name": "Oreo", "search": "oreo cookies box"},
        {"sku": "SNACK002", "name": "Chocopie", "search": "chocopie orion box"},
        {"sku": "SNACK003", "name": "Bánh mì sandwich", "search": "sandwich bread kinh do"},
        {"sku": "SNACK004", "name": "Doublemint", "search": "doublemint chewing gum"},
        {"sku": "SNACK005", "name": "Pringles", "search": "pringles chips original"},
        {"sku": "SNACK006", "name": "AFC", "search": "afc cracker vietnam"},
        {"sku": "SNACK007", "name": "KitKat", "search": "kitkat chocolate bar"},
        {"sku": "SNACK008", "name": "Oishi", "search": "oishi snack shrimp vietnam"},
        {"sku": "SNACK009", "name": "Cosy", "search": "cosy marie biscuit vietnam"},
        {"sku": "SNACK010", "name": "Alpenliebe", "search": "alpenliebe candy"},
    ],
    "mi-an-lien": [
        {"sku": "NOODLE001", "name": "Hảo Hảo", "search": "mi hao hao tom chua cay"},
        {"sku": "NOODLE002", "name": "Omachi", "search": "mi omachi spaghetti"},
        {"sku": "NOODLE003", "name": "Phở Vifon", "search": "pho bo vifon instant"},
        {"sku": "NOODLE004", "name": "Cháo Tươi", "search": "chao tuoi ga instant porridge"},
        {"sku": "NOODLE005", "name": "Mì 3 Miền", "search": "mi 3 mien tom chua cay"},
        {"sku": "NOODLE006", "name": "Kokomi", "search": "mi kokomi vietnam"},
        {"sku": "NOODLE007", "name": "Bún bò Huế Vifon", "search": "bun bo hue vifon instant"},
        {"sku": "NOODLE008", "name": "Mì ly Modern", "search": "mi ly modern cup noodle"},
    ],
    "sua": [
        {"sku": "MILK001", "name": "Vinamilk", "search": "sua tuoi vinamilk hop"},
        {"sku": "MILK002", "name": "TH True Milk", "search": "th true milk box"},
        {"sku": "MILK003", "name": "Sữa chua Vinamilk", "search": "sua chua vinamilk"},
        {"sku": "MILK004", "name": "Sữa đặc Ông Thọ", "search": "sua dac ong tho can"},
        {"sku": "MILK005", "name": "Phô mai con bò cười", "search": "laughing cow cheese"},
        {"sku": "MILK006", "name": "Yakult", "search": "yakult probiotic drink"},
        {"sku": "MILK007", "name": "TH True Nut", "search": "th true nut walnut milk"},
        {"sku": "MILK008", "name": "Bơ Meizan", "search": "meizan margarine butter"},
    ],
    "dong-lanh": [
        {"sku": "FROZEN001", "name": "Kem Merino", "search": "kem merino vietnam"},
        {"sku": "FROZEN002", "name": "Kem Celano", "search": "kem celano vanilla"},
        {"sku": "FROZEN003", "name": "Xúc xích CP", "search": "xuc xich cp frozen"},
        {"sku": "FROZEN004", "name": "Há cảo Bibigo", "search": "bibigo dumpling frozen"},
        {"sku": "FROZEN005", "name": "Đá viên", "search": "ice cubes bag"},
        {"sku": "FROZEN006", "name": "Cornetto", "search": "cornetto ice cream cone"},
    ],
    "gia-vi": [
        {"sku": "SPICE001", "name": "Nước mắm Nam Ngư", "search": "nuoc mam nam ngu bottle"},
        {"sku": "SPICE002", "name": "Tương ớt Chinsu", "search": "tuong ot chinsu bottle"},
        {"sku": "SPICE003", "name": "Dầu ăn Neptune", "search": "dau an neptune cooking oil"},
        {"sku": "SPICE004", "name": "Muối I-ốt", "search": "muoi iot bac lieu salt"},
        {"sku": "SPICE005", "name": "Đường Biên Hòa", "search": "duong bien hoa sugar"},
        {"sku": "SPICE006", "name": "Hạt nêm Knorr", "search": "hat nem knorr vietnam"},
        {"sku": "SPICE007", "name": "Nước tương Maggi", "search": "nuoc tuong maggi soy sauce"},
        {"sku": "SPICE008", "name": "Bột ngọt Ajinomoto", "search": "bot ngot ajinomoto msg"},
    ],
    "cham-soc-ca-nhan": [
        {"sku": "CARE001", "name": "Dầu gội Clear", "search": "dau goi clear men shampoo"},
        {"sku": "CARE002", "name": "Sữa tắm Lifebuoy", "search": "sua tam lifebuoy body wash"},
        {"sku": "CARE003", "name": "Kem đánh răng PS", "search": "kem danh rang ps toothpaste"},
        {"sku": "CARE004", "name": "Giấy vệ sinh Pulppy", "search": "giay ve sinh pulppy toilet paper"},
        {"sku": "CARE005", "name": "Bàn chải Colgate", "search": "ban chai colgate toothbrush"},
        {"sku": "CARE006", "name": "Khăn giấy Kleenex", "search": "khan giay kleenex tissue"},
        {"sku": "CARE007", "name": "Lăn khử mùi Nivea", "search": "lan khu mui nivea men deodorant"},
        {"sku": "CARE008", "name": "Dầu xả Sunsilk", "search": "dau xa sunsilk conditioner"},
    ],
    "gia-dung": [
        {"sku": "HOME001", "name": "Nước rửa chén Sunlight", "search": "nuoc rua chen sunlight dishwashing"},
        {"sku": "HOME002", "name": "Bột giặt OMO", "search": "bot giat omo detergent"},
        {"sku": "HOME003", "name": "Túi rác", "search": "tui rac garbage bag"},
        {"sku": "HOME004", "name": "Nước lau sàn Sunlight", "search": "nuoc lau san sunlight floor cleaner"},
        {"sku": "HOME005", "name": "Pin Energizer", "search": "pin energizer aa battery"},
        {"sku": "HOME006", "name": "Giấy bạc nhôm", "search": "giay bac nhom aluminum foil"},
    ],
    "ruou-bia": [
        {"sku": "ALCOHOL001", "name": "Heineken", "search": "heineken beer can 330ml"},
        {"sku": "ALCOHOL002", "name": "Tiger", "search": "tiger beer can vietnam"},
        {"sku": "ALCOHOL003", "name": "Saigon Special", "search": "bia saigon special can"},
        {"sku": "ALCOHOL004", "name": "Soju Jinro", "search": "jinro soju bottle"},
        {"sku": "ALCOHOL005", "name": "Bia 333", "search": "bia 333 can vietnam"},
    ],
    "thuoc-la": [
        {"sku": "TOBACCO001", "name": "555 Gold", "search": "555 state express cigarettes pack"},
        {"sku": "TOBACCO002", "name": "Vinataba", "search": "vinataba cigarettes vietnam"},
        {"sku": "TOBACCO003", "name": "Marlboro", "search": "marlboro red cigarettes pack"},
        {"sku": "TOBACCO004", "name": "Thăng Long", "search": "thang long cigarettes vietnam"},
    ],
}


def create_placeholder_image(output_path: Path, product_name: str, category: str):
    """Tạo placeholder image nếu không tải được ảnh thật"""
    if not REQUESTS_AVAILABLE:
        print(f"   ⚠️  Không thể tạo placeholder cho {product_name}")
        return False
    
    # Sử dụng placeholder.com để tạo ảnh
    try:
        # Tạo placeholder với text
        url = f"https://placehold.co/400x400/e2e8f0/475569?text={product_name[:15]}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"   ⚠️  Lỗi tạo placeholder: {e}")
    
    return False


def download_with_bing(search_query: str, output_dir: Path, limit: int = 1) -> list:
    """Tải ảnh từ Bing Image Search"""
    if not BING_AVAILABLE:
        return []
    
    try:
        # Tạo thư mục temp
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Download
        downloader.download(
            search_query,
            limit=limit,
            output_dir=str(TEMP_DIR),
            adult_filter_off=True,
            force_replace=False,
            timeout=30,
            verbose=False
        )
        
        # Tìm ảnh đã tải
        search_dir = TEMP_DIR / search_query
        if search_dir.exists():
            images = list(search_dir.glob("*.*"))
            return images
        
    except Exception as e:
        print(f"   ⚠️  Lỗi tải từ Bing: {e}")
    
    return []


def process_category(category_slug: str, dry_run: bool = False):
    """Xử lý tải ảnh cho một category"""
    if category_slug not in PRODUCTS_BY_CATEGORY:
        print(f"❌ Category '{category_slug}' không tồn tại!")
        return
    
    products = PRODUCTS_BY_CATEGORY[category_slug]
    category_dir = UPLOADS_DIR / category_slug
    
    print(f"\n📁 Category: {category_slug} ({len(products)} sản phẩm)")
    print(f"   Output: {category_dir}")
    
    if dry_run:
        for product in products:
            print(f"   [DRY-RUN] {product['sku']}: {product['name']} -> {product['search']}")
        return
    
    # Tạo thư mục
    category_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    for product in products:
        sku = product["sku"]
        name = product["name"]
        search = product["search"]
        output_path = category_dir / f"{sku}.jpg"
        
        # Skip nếu đã có ảnh
        if output_path.exists():
            print(f"   ✓ {sku}: Đã có ảnh")
            success_count += 1
            continue
        
        print(f"   🔄 {sku}: Đang tải '{search}'...")
        
        # Thử tải từ Bing
        images = download_with_bing(search, category_dir, limit=IMAGES_PER_PRODUCT)
        
        if images:
            # Copy ảnh đầu tiên
            try:
                shutil.copy(images[0], output_path)
                print(f"   ✅ {sku}: Saved to {output_path.name}")
                success_count += 1
            except Exception as e:
                print(f"   ❌ {sku}: Lỗi copy - {e}")
        else:
            # Fallback: tạo placeholder
            print(f"   ⚠️  {sku}: Không tìm thấy ảnh, tạo placeholder...")
            if create_placeholder_image(output_path, name, category_slug):
                print(f"   ✅ {sku}: Placeholder created")
                success_count += 1
            else:
                print(f"   ❌ {sku}: Không thể tạo ảnh")
        
        # Rate limiting
        time.sleep(1)
    
    print(f"   📊 Hoàn thành: {success_count}/{len(products)} ảnh")


def cleanup_temp():
    """Xóa thư mục temp"""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        print(f"\n🧹 Đã xóa thư mục temp: {TEMP_DIR}")


def create_gitkeep_files():
    """Tạo .gitkeep files để git track thư mục trống"""
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Root gitkeep
    gitkeep_root = UPLOADS_DIR / ".gitkeep"
    if not gitkeep_root.exists():
        gitkeep_root.touch()
    
    # Category gitkeeps
    for category in PRODUCTS_BY_CATEGORY.keys():
        category_dir = UPLOADS_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = category_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()


def main():
    parser = argparse.ArgumentParser(description="Download product images cho cửa hàng tiện lợi")
    parser.add_argument("--category", "-c", help="Chỉ download cho category cụ thể")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Chỉ hiển thị, không tải")
    parser.add_argument("--list", "-l", action="store_true", help="Liệt kê các categories")
    parser.add_argument("--cleanup", action="store_true", help="Xóa thư mục temp")
    
    args = parser.parse_args()
    
    # Liệt kê categories
    if args.list:
        print("\n📋 Danh sách categories:")
        for cat, products in PRODUCTS_BY_CATEGORY.items():
            print(f"   - {cat}: {len(products)} sản phẩm")
        return
    
    # Cleanup temp
    if args.cleanup:
        cleanup_temp()
        return
    
    print("=" * 60)
    print("🏪 IMAGE DOWNLOADER - CỬA HÀNG TIỆN LỢI")
    print("=" * 60)
    
    if not BING_AVAILABLE:
        print("\n⚠️  bing-image-downloader chưa được cài đặt!")
        print("   Chạy: pip install bing-image-downloader")
        print("   Sẽ sử dụng placeholder images thay thế.\n")
    
    # Tạo gitkeep files
    create_gitkeep_files()
    
    # Process categories
    if args.category:
        process_category(args.category, args.dry_run)
    else:
        for category in PRODUCTS_BY_CATEGORY.keys():
            process_category(category, args.dry_run)
    
    # Cleanup
    if not args.dry_run:
        cleanup_temp()
    
    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH!")
    print("=" * 60)


if __name__ == "__main__":
    main()
