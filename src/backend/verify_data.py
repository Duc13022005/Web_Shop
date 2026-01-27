
import asyncio
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_DATA")

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import text, select, func
from core.database import async_session_maker
from catalog.models import Product, Category
# Import all models to ensure SQLAlchemy registry is populated
from users.models import User
from orders.models import Order
from inventory.models import InventoryBatch

async def verify_data():
    logger.info("📦 CHECKING DATA INTEGRITY...")
    
    async with async_session_maker() as db:
        # Check Categories
        result = await db.execute(select(func.count(Category.id)))
        cat_count = result.scalar()
        logger.info(f"📂 Categories Count: {cat_count}")
        
        if cat_count > 0:
            cats = await db.execute(select(Category).limit(5))
            for c in cats.scalars():
                logger.info(f"   - {c.name} (ID: {c.id})")
        else:
            logger.error("❌ NO CATEGORIES FOUND!")

        # Check Products
        result = await db.execute(select(func.count(Product.id)))
        prod_count = result.scalar()
        logger.info(f"🍎 Products Count: {prod_count}")
        
        if prod_count > 0:
            prods = await db.execute(select(Product).limit(5))
            for p in prods.scalars():
                logger.info(f"   - {p.name} (SKU: {p.sku}, Price: {p.base_price})")
        else:
            logger.error("❌ NO PRODUCTS FOUND!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_data())

