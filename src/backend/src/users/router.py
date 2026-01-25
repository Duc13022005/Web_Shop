"""
User API Router
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.users.models import UserRole
from src.users.schemas import UserResponse, UserListResponse, UserAdminUpdate
from src.users.service import UserService
from src.auth.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/users")


@router.get("", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    List all users (Admin only)
    
    - Supports pagination and filtering by role/status
    """
    skip = (page - 1) * size
    users, total = await UserService.get_all(db, skip=skip, limit=size, role=role, is_active=is_active)
    
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        size=size
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Get user by ID (Admin only)
    """
    from src.core.exceptions import NotFoundException
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserAdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Update user (Admin only)
    
    - Can update email, password, role, and status
    """
    user = await UserService.admin_update(db, user_id, user_data)
    return UserResponse.model_validate(user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Soft delete user (Admin only)
    
    - Sets is_active=False instead of hard delete
    """
    await UserService.delete(db, user_id)
    return {"message": "User deactivated successfully"}
