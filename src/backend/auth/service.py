"""
Authentication Service
"""

from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User, UserRole
from users.schemas import UserCreate
from users.service import UserService
from core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token,
)
from core.exceptions import UnauthorizedException, BadRequestException
from auth.schemas import TokenResponse


class AuthService:
    """Authentication business logic"""
    
    @staticmethod
    async def register(
        db: AsyncSession,
        email: str,
        password: str,
        full_name: str,
        phone: str | None = None,
        address: str | None = None,
    ) -> User:
        """Register a new user"""
        user_data = UserCreate(
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            address=address,
            role=UserRole.customer
        )
        return await UserService.create(db, user_data)
    
    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> tuple[User, TokenResponse]:
        """
        Authenticate user and return tokens.
        
        Returns:
            Tuple of (User, TokenResponse)
        
        Raises:
            UnauthorizedException: If credentials are invalid
        """
        user = await UserService.authenticate(db, email, password)
        if not user:
            raise UnauthorizedException(detail="Invalid email or password")
        
        tokens = AuthService.create_tokens(user)
        return user, tokens
    
    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """Create access and refresh tokens for user"""
        token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    @staticmethod
    async def refresh_tokens(db: AsyncSession, refresh_token: str) -> TokenResponse:
        """
        Refresh access token using refresh token.
        
        Returns:
            New TokenResponse
        
        Raises:
            UnauthorizedException: If refresh token is invalid
        """
        payload = verify_token(refresh_token, token_type="refresh")
        if payload is None:
            raise UnauthorizedException(detail="Invalid or expired refresh token")
        
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException(detail="Invalid token payload")
        
        user = await UserService.get_by_id(db, int(user_id))
        if user is None or not user.is_active:
            raise UnauthorizedException(detail="User not found or inactive")
        
        return AuthService.create_tokens(user)
    
    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Returns:
            True if successful
        
        Raises:
            BadRequestException: If current password is incorrect
        """
        if not verify_password(current_password, user.password_hash):
            raise BadRequestException(detail="Current password is incorrect")
        
        user.password_hash = get_password_hash(new_password)
        await db.commit()
        return True

