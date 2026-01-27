"""Auth module initialization"""
from auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from auth.service import AuthService
from auth.dependencies import get_current_user, require_roles

