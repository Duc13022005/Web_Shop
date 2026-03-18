import os
import sys
import asyncio
from datetime import datetime

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.future import select
from core.database import engine, Base, async_session_maker
from core.security import get_password_hash
from models import User, UserRole, Employee, EmployeeRole

async def setup_database():
    print("Creating tables if they don't exist...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

async def create_admin():
    email = input("Admin Email [admin@7comart.com]: ") or "admin@7comart.com"
    password = input("Admin Password [admin123]: ") or "admin123"
    full_name = input("Admin Full Name [Administrator]: ") or "Administrator"

    async with async_session_maker() as session:
        # Check if admin already exists
        result = await session.execute(select(User).filter(User.email == email))
        admin_user = result.scalars().first()
        if admin_user:
            print(f"Admin user {email} already exists.")
            return

        new_admin = User(
            email=email,
            password_hash=get_password_hash(password),
            full_name=full_name,
            role=UserRole.admin,
            is_active=True
        )
        session.add(new_admin)
        await session.commit()
        print(f"Admin user {email} created successfully!")

async def create_mock_employees():
    async with async_session_maker() as session:
        result = await session.execute(select(Employee))
        if len(result.scalars().all()) > 0:
            print("Employees already exist. Skipping mock data.")
            return

        employees_data = [
            {"full_name": "Nguyễn Văn Shipper", "email": "shipper1@7comart.com", "phone": "0987654321", "role": EmployeeRole.shipper, "salary": 8000000},
            {"full_name": "Trần Thị Thu Ngân", "email": "thungan1@7comart.com", "phone": "0912345678", "role": EmployeeRole.cashier, "salary": 7000000},
            {"full_name": "Lê Cô Vệ Sinh", "email": "vesinh1@7comart.com", "phone": "0923456789", "role": EmployeeRole.cleaner, "salary": 6000000},
            {"full_name": "Phạm Anh Shipper", "email": "shipper2@7comart.com", "phone": "0945678901", "role": EmployeeRole.shipper, "salary": 8000000},
            {"full_name": "Hoàng Chị Thu Ngân", "email": "thungan2@7comart.com", "phone": "0956789012", "role": EmployeeRole.cashier, "salary": 7000000},
        ]

        for data in employees_data:
            emp = Employee(**data)
            session.add(emp)

        await session.commit()
        print("Mock HR employees created successfully!")

async def main():
    print("=== Admin & HR Setup ===")
    await setup_database()
    await create_admin()
    await create_mock_employees()
    print("=== Setup Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
