
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from auth.service import AuthService
from core.security import verify_password, get_password_hash
from users.service import UserService
# Import other models to ensure SQLAlchemy registry is populated for relationships
from orders.models import Order
from catalog.models import Product, Category

# Local host connection string
LOCAL_DB_URL = "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db"

async def test_auth():
    print(f"🚀 Connecting to database...")
    engine = create_async_engine(LOCAL_DB_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as db:
        try:
            print("🔍 Testing User Retrieval...")
            user = await UserService.get_by_email(db, "admin@example.com")
            if not user:
                print("❌ User 'admin@example.com' NOT FOUND in DB.")
                return
            
            print(f"✅ User found: {user.email}")
            print(f"Password Hash in DB: {user.password_hash}")
            
            print("🔐 Testing Password Verification (Direct)...")
            is_valid = verify_password("admin123", user.password_hash)
            print(f"Direct Verify 'admin123': {'✅ VALID' if is_valid else '❌ INVALID'}")
            
            if not is_valid:
                print("DEBUG: Generating new hash for 'admin123' to compare...")
                new_hash = get_password_hash("admin123")
                print(f"New Hash: {new_hash}")
                
            print("🔑 Testing AuthService.login()...")
            try:
                user, tokens = await AuthService.login(db, "admin@example.com", "admin123")
                print("✅ AuthService.login SUCCESS!")
                print(f"Access Token: {tokens.access_token[:20]}...")
            except Exception as e:
                print(f"❌ AuthService.login FAILED: {e}")

        except Exception as e:
            print(f"❌ Error during test: {e}")
        finally:
            await engine.dispose()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_auth())

