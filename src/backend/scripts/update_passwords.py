
import asyncio
import sys
import os

# Add src to python path
sys.path.append(os.getcwd())

from sqlalchemy import select
from core.database import async_session_maker
from models import User
from core.security import get_password_hash

async def update_passwords():
    print("🔄 Updating passwords to Argon2 hashes...")
    
    new_hash = get_password_hash("password123")
    emails = ["admin@shop.vn", "staff1@shop.vn", "khach1@gmail.com"]
    
    async with async_session_maker() as session:
        for email in emails:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user:
                user.password_hash = new_hash
                print(f"✅ Updated password for {email}")
            else:
                print(f"⚠️ User {email} not found")
        
        await session.commit()
    print("✨ Password update complete!")

if __name__ == "__main__":
    asyncio.run(update_passwords())

