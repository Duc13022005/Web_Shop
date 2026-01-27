"""
Authentication API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from users.models import User
from users.schemas import UserResponse
from auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordChangeRequest,
    AuthResponse,
)
from auth.service import AuthService
from auth.dependencies import get_current_user

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=AuthResponse)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - Creates a new customer account
    - Returns user info and authentication tokens
    """
    user = await AuthService.register(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
        phone=request.phone,
        address=request.address,
    )
    tokens = AuthService.create_tokens(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    - Returns user info and authentication tokens
    """
    user, tokens = await AuthService.login(db, request.email, request.password)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - Returns new access and refresh tokens
    """
    return await AuthService.refresh_tokens(db, request.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user info.
    
    - Requires valid access token
    """
    return UserResponse.model_validate(current_user)


@router.put("/change-password")
async def change_password(
    request: PasswordChangeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change password for current user.
    
    - Requires current password for verification
    """
    await AuthService.change_password(
        db=db,
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password
    )
    return {"message": "Password changed successfully"}

