"""
Authentication Pydantic Schemas
"""

from pydantic import BaseModel, EmailStr, Field

from users.schemas import UserResponse


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    """Registration request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: str | None = Field(None, max_length=20)
    address: str | None = None


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


class AuthResponse(BaseModel):
    """Auth response with user and tokens"""
    user: UserResponse
    tokens: TokenResponse

