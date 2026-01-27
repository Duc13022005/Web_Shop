"""
User SQLAlchemy Model
"""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from core.database import Base

if TYPE_CHECKING:
    from orders.models import Order, Cart


class UserRole(str, enum.Enum):
    """User role enumeration - values must match PostgreSQL enum exactly"""
    customer = "customer"
    staff = "staff"
    admin = "admin"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", create_type=False),
        default=UserRole.customer
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (string references to avoid circular imports)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")
    cart: Mapped[Optional["Cart"]] = relationship("Cart", back_populates="user", uselist=False)
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

