"""
Authentication Dependencies
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import verify_token
from core.exceptions import UnauthorizedException, ForbiddenException
from users.models import User, UserRole
from users.service import UserService


# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Raises:
        UnauthorizedException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise UnauthorizedException(detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException(detail="Invalid token payload")
    
    user = await UserService.get_by_id(db, int(user_id))
    if user is None:
        raise UnauthorizedException(detail="User not found")
    
    if not user.is_active:
        raise UnauthorizedException(detail="User is inactive")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise ForbiddenException(detail="Inactive user")
    return current_user


def require_roles(allowed_roles: List[UserRole]):
    """
    Dependency factory for role-based access control.
    
    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(user = Depends(require_roles([UserRole.ADMIN]))):
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


# Convenience dependencies
require_admin = require_roles([UserRole.admin])
require_staff = require_roles([UserRole.admin, UserRole.staff])
require_customer = require_roles([UserRole.admin, UserRole.staff, UserRole.customer])

