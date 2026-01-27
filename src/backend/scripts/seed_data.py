
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from core.database import async_session_maker
from users.service import UserService
from users.schemas import UserCreate
from users.models import UserRole

async def seed():
    print("🚀 Seeding Data...")
    async with async_session_maker() as db:
        try:
            print("👤 Checking/Creating Admin User...")
            admin_data = UserCreate(
                email="admin@example.com",
                password="admin123",
                full_name="Admin User",
                phone="0999999999",
                address="123 Docker St",
                role=UserRole.admin
            )
            
            try:
                user = await UserService.create(db, admin_data)
                print(f"✅ Admin Created: {user.email}")
            except Exception as e:
                print(f"⚠️  Admin creation skipped (likely exists): {e}")

        except Exception as e:
            print(f"❌ Error during seeding: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())

