
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.users.service import UserService
from src.users.schemas import UserCreate
from src.users.models import UserRole

# Local host connection string
LOCAL_DB_URL = "postgresql+asyncpg://shop_user:shop_password_123@localhost:5433/shop_db"

async def seed():
    print(f"🚀 Connecting to database at: {LOCAL_DB_URL.replace('shop_password_123', '***')}")
    
    # Create isolated engine/session for this script
    engine = create_async_engine(LOCAL_DB_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as db:
        try:
            print("👤 Checking for existing admin user...")
            
            # Create user data
            admin_data = UserCreate(
                email="admin@example.com",
                password="admin123",
                full_name="Admin Test",
                phone="0123456789",
                address="123 Test St",
                role=UserRole.admin
            )
            
            # Attempt creation
            try:
                user = await UserService.create(db, admin_data)
                print(f"✅ SUCCESS: Admin user created: {user.email} / admin123")
            except Exception as e:
                # If create fails, it might exist. Let's try to verify?
                # But UserService doesn't strictly check existence before insert usually, 
                # depends on if email is unique constrained and handled.
                print(f"⚠️  User creation skipped (might already exist): {e}")
                
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
        finally:
            await engine.dispose()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
