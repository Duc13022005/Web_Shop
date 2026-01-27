
import asyncio
import sys
import os
import random
from datetime import date, timedelta
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from catalog.models import Category, Product
from inventory.models import InventoryBatch
# Import other models to ensure registry is populated
from users.models import User
from orders.models import Order

# Database Connection String
DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db")

# Product Data (Copied from download_images.py)
PRODUCTS_BY_CATEGORY = {
    "do-uong": [
        {"sku": "DRINK001", "name": "Coca-Cola", "price": 10000},
        {"sku": "DRINK002", "name": "Pepsi", "price": 10000},
        {"sku": "DRINK003", "name": "Trà xanh 0 độ", "price": 12000},
        {"sku": "DRINK004", "name": "Lavie", "price": 5000},
        {"sku": "DRINK005", "name": "Teppy", "price": 15000},
        {"sku": "DRINK006", "name": "Highlands Coffee", "price": 18000},
        {"sku": "DRINK007", "name": "Red Bull", "price": 12000},
        {"sku": "DRINK008", "name": "Sting", "price": 10000},
        {"sku": "DRINK009", "name": "Fuze Tea", "price": 12000},
        {"sku": "DRINK010", "name": "Cocoxim", "price": 20000},
        {"sku": "DRINK011", "name": "Aquafina", "price": 5000},
        {"sku": "DRINK012", "name": "C2", "price": 8000},
        {"sku": "DRINK013", "name": "Nước yến Sante", "price": 25000},
        {"sku": "DRINK014", "name": "Revive", "price": 10000},
        {"sku": "DRINK015", "name": "Fanta", "price": 10000},
    ],
    "banh-keo": [
        {"sku": "SNACK001", "name": "Oreo", "price": 15000},
        {"sku": "SNACK002", "name": "Chocopie", "price": 35000},
        {"sku": "SNACK003", "name": "Bánh mì sandwich", "price": 20000},
        {"sku": "SNACK004", "name": "Doublemint", "price": 5000},
        {"sku": "SNACK005", "name": "Pringles", "price": 40000},
        {"sku": "SNACK006", "name": "AFC", "price": 25000},
        {"sku": "SNACK007", "name": "KitKat", "price": 15000},
        {"sku": "SNACK008", "name": "Oishi", "price": 6000},
        {"sku": "SNACK009", "name": "Cosy", "price": 25000},
        {"sku": "SNACK010", "name": "Alpenliebe", "price": 5000},
    ],
    "mi-an-lien": [
        {"sku": "NOODLE001", "name": "Hảo Hảo", "price": 4000},
        {"sku": "NOODLE002", "name": "Omachi", "price": 7000},
        {"sku": "NOODLE003", "name": "Phở Vifon", "price": 15000},
        {"sku": "NOODLE004", "name": "Cháo Tươi", "price": 20000},
        {"sku": "NOODLE005", "name": "Mì 3 Miền", "price": 3000},
        {"sku": "NOODLE006", "name": "Kokomi", "price": 3000},
        {"sku": "NOODLE007", "name": "Bún bò Huế Vifon", "price": 15000},
        {"sku": "NOODLE008", "name": "Mì ly Modern", "price": 8000},
    ],
    "sua": [
        {"sku": "MILK001", "name": "Vinamilk", "price": 30000},
        {"sku": "MILK002", "name": "TH True Milk", "price": 32000},
        {"sku": "MILK003", "name": "Sữa chua Vinamilk", "price": 6000},
        {"sku": "MILK004", "name": "Sữa đặc Ông Thọ", "price": 25000},
        {"sku": "MILK005", "name": "Phô mai con bò cười", "price": 45000},
        {"sku": "MILK006", "name": "Yakult", "price": 25000},
        {"sku": "MILK007", "name": "TH True Nut", "price": 40000},
        {"sku": "MILK008", "name": "Bơ Meizan", "price": 30000},
    ],
    "dong-lanh": [
        {"sku": "FROZEN001", "name": "Kem Merino", "price": 10000},
        {"sku": "FROZEN002", "name": "Kem Celano", "price": 15000},
        {"sku": "FROZEN003", "name": "Xúc xích CP", "price": 40000},
        {"sku": "FROZEN004", "name": "Há cảo Bibigo", "price": 60000},
        {"sku": "FROZEN005", "name": "Đá viên", "price": 10000},
        {"sku": "FROZEN006", "name": "Cornetto", "price": 18000},
    ],
}

async def seed_products():
    print(f"🚀 Connecting to DB: {DB_URL.replace('shop_password_123', '***')}")
    engine = create_async_engine(DB_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        for cat_slug, products in PRODUCTS_BY_CATEGORY.items():
            # 1. Ensure Category
            print(f"📂 Processing Category: {cat_slug}")
            result = await db.execute(select(Category).where(Category.slug == cat_slug))
            category = result.scalar_one_or_none()
            
            if not category:
                category = Category(
                    name=cat_slug.replace("-", " ").title(),
                    slug=cat_slug,
                    description=f"Danh mục {cat_slug}",
                    sort_order=1
                )
                db.add(category)
                await db.commit()
                await db.refresh(category)
                print(f"   ✅ Created Category: {category.name}")
            else:
                print(f"   ℹ️  Category exists: {category.name}")

            # 2. Ensure Products
            for p_data in products:
                result = await db.execute(select(Product).where(Product.sku == p_data["sku"]))
                product = result.scalar_one_or_none()
                
                if not product:
                    product = Product(
                        sku=p_data["sku"],
                        name=p_data["name"],
                        category_id=category.id,
                        base_price=Decimal(p_data["price"]),
                        sale_price=None,
                        unit="cái",
                        is_active=True
                    )
                    db.add(product)
                    await db.commit()
                    await db.refresh(product)
                    print(f"   ✅ Created Product: {product.name}")
                else:
                    print(f"   ℹ️  Product exists: {product.name}")
                    
                # 3. Ensure Inventory
                # Check directly via select count to identify if we need to add stock
                # OR check via relationship if loaded, but safer to just query
                batch_res = await db.execute(select(InventoryBatch).where(InventoryBatch.product_id == product.id))
                batches = batch_res.scalars().all()
                
                if not batches:
                    batch = InventoryBatch(
                        product_id=product.id,
                        batch_code=f"BATCH-{date.today().strftime('%Y%m%d')}-{product.id}",
                        expiry_date=date.today() + timedelta(days=365),
                        quantity_on_hand=100,
                        quantity_reserved=0,
                        cost_price=Decimal(p_data["price"]) * Decimal("0.7"), # 70% cost
                        received_date=date.today()
                    )
                    db.add(batch)
                    await db.commit()
                    print(f"   📦 Added Inventory: 100 items for {product.name}")

    await engine.dispose()
    print("✨ Seeding Complete!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_products())

