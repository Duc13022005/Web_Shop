"""Auth module initialization"""
from src.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from src.auth.service import AuthService
from src.auth.dependencies import get_current_user, require_roles
