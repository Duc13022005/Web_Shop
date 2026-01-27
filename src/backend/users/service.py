"""
User Service - Business Logic
"""

from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User, UserRole
from users.schemas import UserCreate, UserUpdate, UserAdminUpdate
from core.security import get_password_hash, verify_password
from core.exceptions import NotFoundException, ConflictException


class UserService:
    """User business logic"""
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 20,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> tuple[List[User], int]:
        """Get all users with pagination and filters"""
        query = select(User)
        count_query = select(func.count(User.id))
        
        if role:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(User.id)
        result = await db.execute(query)
        users = result.scalars().all()
        
        return list(users), total
    
    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email exists
        existing = await UserService.get_by_email(db, user_data.email)
        if existing:
            raise ConflictException(detail="Email already registered")
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address,
            role=user_data.role,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
        """Update user"""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise NotFoundException(detail="User not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def admin_update(db: AsyncSession, user_id: int, user_data: UserAdminUpdate) -> User:
        """Admin update user (including password and email)"""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise NotFoundException(detail="User not found")
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Handle password separately
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        # Check email uniqueness
        if "email" in update_data and update_data["email"] != user.email:
            existing = await UserService.get_by_email(db, update_data["email"])
            if existing:
                raise ConflictException(detail="Email already registered")
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Soft delete user (set is_active=False)"""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise NotFoundException(detail="User not found")
        
        user.is_active = False
        await db.commit()
        return True
    
    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        print(f"--- DEBUG AUTH: Login attempt for '{email}' ---")
        user = await UserService.get_by_email(db, email)
        if not user:
            print(f"--- DEBUG AUTH: User '{email}' NOT FOUND in database ---")
            return None
            
        print(f"--- DEBUG AUTH: User found. ID: {user.id}, Role: {user.role} ---")
        print(f"--- DEBUG AUTH: Stored Hash: {user.password_hash} ---")
        
        is_valid = verify_password(password, user.password_hash)
        if not is_valid:
            print(f"--- DEBUG AUTH: Password verification FAILED for '{email}' ---")
            return None
            
        if not user.is_active:
            print(f"--- DEBUG AUTH: User '{email}' is INACTIVE ---")
            return None
            
        print(f"--- DEBUG AUTH: Success! Authenticated '{email}' ---")
        return user

