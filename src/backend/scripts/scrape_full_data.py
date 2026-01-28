
import asyncio
import sys
import os
import shutil
import json
import random
from pathlib import Path
from typing import List, Dict

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload

try:
    from bing_image_downloader import downloader
    BING_AVAILABLE = True
except ImportError:
    BING_AVAILABLE = False
    print("⚠️  bing-image-downloader not installed. Images won't be downloaded.")

from catalog.models import Product, Category
from users.models import User
from orders.models import Order
from inventory.models import InventoryBatch

# Database Connection
DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db")
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"

# Rich descriptions and specs for random generation if not real
RICH_SPECS = {
    "do-uong": {"volume": "330ml", "origin": "Vietnam", "brand": "Coca-Cola Company", "ingredients": "Nước bão hòa CO2, đường HFCS, đường mía, màu thực phẩm"},
    "banh-keo": {"weight": "100g", "origin": "Korea", "brand": "Orion", "ingredients": "Bột mì, Đường, Socola, Bơ thực vật"},
    "mi-an-lien": {"weight": "75g", "origin": "Vietnam", "brand": "Acecook", "ingredients": "Bột mì, tinh bột khoai mì, dầu cọ, muối, đường"},
    "thit-ca": {"weight": "500g", "origin": "Vietnam", "storage": "Ngăn đông"},
    "trung-sua": {"volume": "1L", "origin": "Vinamilk", "storage": "Ngăn mát"},
    "rau-cu": {"weight": "1kg", "origin": "Dalat", "quality": "VietGAP"},
    "do-dong-lanh": {"weight": "500g", "storage": "-18 độ C"},
    "an-vat": {"weight": "50g", "origin": "Vietnam", "ingredients": "Đậu phộng, muối, gia vị"},
    "cham-soc-ca-nhan": {"volume": "200ml", "origin": "Unilever"},
}

async def scrape_product_images(product_name: str, limit: int = 3) -> List[str]:
    """Download images from Bing"""
    if not BING_AVAILABLE:
        return []
    
    query = f"{product_name} vietnam product"
    output_dir = UPLOADS_DIR / "temp_scrape"
    
    print(f"   ⬇️  Downloading {limit} images for '{product_name}'...")
    try:
        downloader.download(
            query, 
            limit=limit, 
            output_dir=str(output_dir), 
            adult_filter_off=True, 
            force_replace=False, 
            timeout=10, 
            verbose=False
        )
        
        # Find downloaded files
        downloaded_dir = output_dir / query
        if downloaded_dir.exists():
            return sorted([str(p) for p in downloaded_dir.glob("*.*")])
            
    except Exception as e:
        print(f"   ❌ Download error: {e}")
        
    return []

async def process_products():
    print(f"🚀 Connecting to DB: {DB_URL.replace('shop_password_123', '***')}")
    engine = create_async_engine(DB_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        # Fetch all products with category
        result = await db.execute(select(Product).options(selectinload(Product.category)).order_by(Product.id))
        products = result.scalars().all()
        
        print(f"📦 Processing {len(products)} products...")
        
        for product in products:
            if not product.category:
                continue

            print(f"\n🔄 Processing: {product.name} ({product.sku})")
            cat_slug = product.category.slug
            product_upload_dir = UPLOADS_DIR / cat_slug
            product_upload_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. Scrape Images
            # Check if we already have images in DB
            if not product.images or len(product.images) < 3:
                downloaded_files = await scrape_product_images(product.name, limit=4)
                
                final_image_paths = []
                for idx, src_path in enumerate(downloaded_files):
                    ext = Path(src_path).suffix
                    new_filename = f"{product.sku}_{idx+1}{ext}"
                    dest_path = product_upload_dir / new_filename
                    
                    try:
                        shutil.copy(src_path, dest_path)
                        # Relative path for API
                        rel_path = f"{cat_slug}/{new_filename}"
                        final_image_paths.append(rel_path)
                    except Exception as e:
                        print(f"   ❌ Copy error: {e}")

                if final_image_paths:
                    # Update DB
                    product.images = final_image_paths
                    # Set main image if not set
                    if not product.image_path:
                        product.image_path = final_image_paths[0]
                    print(f"   ✅ Updated images: {len(final_image_paths)} files")
                
                # Cleanup temp
                shutil.rmtree(UPLOADS_DIR / "temp_scrape", ignore_errors=True)

            # 2. Generate Specifications
            if not product.specifications:
                base_specs = RICH_SPECS.get(cat_slug, {"origin": "Vietnam"})
                # Add some randomness
                specs = base_specs.copy()
                specs["expiry"] = f"{random.randint(6, 12)} months"
                specs["manufacture_date"] = "2024-01-01"
                
                product.specifications = specs
                print(f"   ✅ Updated specifications")

            # 3. Update Description if empty or broken
            if not product.description or product.id == 1 or "?" in product.description:
                product.description = f"Sản phẩm {product.name} chính hãng. Hương vị tuyệt hảo, nguyên liệu tự nhiên được chọn lọc kỹ càng. Phù hợp cho bữa ăn gia đình và các dịp tụ tập bạn bè. Cam kết chất lượng từ nhà sản xuất."
                print(f"   ✅ Updated description")

            await db.commit()
    
    await engine.dispose()
    print("\n✨ Scraping & Enrichment Complete!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(process_products())
