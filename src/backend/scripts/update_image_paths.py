
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog.models import Product, Category
from users.models import User
from orders.models import Order
from inventory.models import InventoryBatch

# Database Connection String
DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db")
UPLOADS_DIR = Path("uploads")

async def update_image_paths():
    print(f"🚀 Connecting to DB: {DB_URL.replace('shop_password_123', '***')}")
    engine = create_async_engine(DB_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        print("🔍 Checking products...")
        from sqlalchemy.orm import selectinload
        result = await db.execute(select(Product).options(selectinload(Product.category)).order_by(Product.id))
        products = result.scalars().all()
        
        count = 0
        for product in products:
            if not product.category:
                continue
            
            cat_slug = product.category.slug
            expected_filename = f"{product.sku}.jpg"
            # In DB we want relative path: "category_slug/sku.jpg"
            image_path = f"{cat_slug}/{expected_filename}"
            
            if product.image_path != image_path:
                print(f"   🔄 Updating {product.sku}: {product.image_path} -> {image_path}")
                product.image_path = image_path
                count += 1
            else:
                pass
                # print(f"   ✓ {product.sku} OK")

        if count > 0:
            await db.commit()
            print(f"✅ Updated {count} product image paths.")
        else:
            print("✅ All product image paths are already correct.")

    await engine.dispose()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(update_image_paths())
