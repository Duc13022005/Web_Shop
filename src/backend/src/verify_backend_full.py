
import asyncio
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_BACKEND")

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy import text
from src.core.database import async_session_maker, engine
from src.users.service import UserService
from src.core.security import verify_password
from src.users.models import UserRole

# Import all models to ensure SQLAlchemy registry is populated
from src.orders.models import Order
from src.inventory.models import InventoryBatch
from src.catalog.models import Product, Category

async def verify_system():
    logger.info("🚀 STARTING SYSTEM VERIFICATION")
    
    # 1. Test Database Connection
    logger.info("------------------------------------------------")
    logger.info("STEP 1: Testing Database Connection...")
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info(f"✅ Database Connected! Result: {result.scalar()}")
    except Exception as e:
        logger.error(f"❌ Database Connection Failed: {e}")
        return

    # 2. Test User Existence and Data
    logger.info("------------------------------------------------")
    logger.info("STEP 2: Verifying Admin User Data...")
    async with async_session_maker() as db:
        user = await UserService.get_by_email(db, "admin@example.com")
        if not user:
            logger.error("❌ User 'admin@example.com' NOT FOUND.")
            return
        
        logger.info(f"✅ User Found: ID={user.id}, Email={user.email}")
        logger.info(f"   Role: {user.role}")
        logger.info(f"   Is Active: {user.is_active}")
        logger.info(f"   Password Hash: {user.password_hash}")

        # 3. Test Password Verification
        logger.info("------------------------------------------------")
        logger.info("STEP 3: Testing Password Verification...")
        TEST_PASS = "admin123"
        is_valid = verify_password(TEST_PASS, user.password_hash)
        
        if is_valid:
            logger.info(f"✅ Password '{TEST_PASS}' MATCHES the hash.")
        else:
            logger.error(f"❌ Password '{TEST_PASS}' DOES NOT MATCH the hash.")
            return

        # 4. Test AuthService Logic
        logger.info("------------------------------------------------")
        logger.info("STEP 4: Testing UserService.authenticate()...")
        try:
            auth_user = await UserService.authenticate(db, "admin@example.com", "admin123")
            if auth_user:
                logger.info(f"✅ UserService.authenticate SUCCESS! Returned User ID: {auth_user.id}")
            else:
                logger.error("❌ UserService.authenticate FAILED (Returned None).")
        except Exception as e:
            logger.error(f"❌ UserService.authenticate CRASHED: {e}")

    logger.info("------------------------------------------------")
    logger.info("🏁 VERIFICATION COMPLETE")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_system())
