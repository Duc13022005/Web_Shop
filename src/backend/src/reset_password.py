
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.core.database import async_session_maker
from src.users.service import UserService
from src.core.security import get_password_hash, verify_password

# Import all models to ensure SQLAlchemy registry is populated
from src.users.models import User
from src.orders.models import Order
from src.catalog.models import Product, Category
# from src.reviews.models import Review # Add if exists

async def reset_password():
    print("🛠️  Force Resetting Admin Password...")
    async with async_session_maker() as db:
        try:
            print("🔍 Finding Admin User...")
            user = await UserService.get_by_email(db, "admin@example.com")
            
            if not user:
                print("❌ Admin user NOT FOUND! Creating it...")
                # We could create, but seed should have done it.
                # Let's focus on reset.
                return

            print(f"✅ User Found: {user.email}")
            print(f"   Current Hash: {user.password_hash}")
            
            new_password = "admin123"
            new_hash = get_password_hash(new_password)
            
            print(f"🔑 Setting new password: '{new_password}'")
            user.password_hash = new_hash
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            print("💾 Password updated in DB.")
            
            # Verify immediately
            is_valid = verify_password(new_password, user.password_hash)
            print(f"✅ Verification check: {'PASSED' if is_valid else 'FAILED'}")

        except Exception as e:
            print(f"❌ Error during reset: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(reset_password())
