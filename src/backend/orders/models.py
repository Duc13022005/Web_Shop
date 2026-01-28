"""
Orders SQLAlchemy Models - Order, OrderItem, Cart, CartItem
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Text, Numeric, Integer, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from core.database import Base

if TYPE_CHECKING:
    from users.models import User
    from catalog.models import Product
    from inventory.models import InventoryBatch


class OrderStatus(str, enum.Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PICKING = "picking"
    DELIVERING = "delivering"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    """Payment method enumeration"""
    COD = "cod"
    MOMO = "momo"
    VNPAY = "vnpay"
    BANK_TRANSFER = "bank_transfer"


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Order(Base):
    """Order model"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status", create_type=False),
        default=OrderStatus.PENDING
    )
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    delivery_fee: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    delivery_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    customer_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    customer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod, name="payment_method", create_type=False),
        default=PaymentMethod.COD
    )
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus, name="payment_status", create_type=False),
        default=PaymentStatus.PENDING
    )
    is_age_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    @property
    def total_items(self) -> int:
        """Get total number of items"""
        return sum(item.quantity for item in self.items)
    
    def __repr__(self) -> str:
        return f"<Order #{self.id} - {self.status.value}>"


class OrderItem(Base):
    """Order item model"""
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    batch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("inventory_batches.id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price_at_purchase: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    batch: Mapped[Optional["InventoryBatch"]] = relationship("InventoryBatch", back_populates="order_items")
    
    def __repr__(self) -> str:
        return f"<OrderItem {self.product_id} x {self.quantity}>"


class Cart(Base):
    """Shopping cart model"""
    __tablename__ = "carts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    
    @property
    def total_items(self) -> int:
        """Get total number of items"""
        return sum(item.quantity for item in self.items)
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal"""
        return sum(item.subtotal for item in self.items)
    
    def __repr__(self) -> str:
        return f"<Cart user={self.user_id}>"


class CartItem(Base):
    """Cart item model"""
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_item_product"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate item subtotal"""
        if self.product:
            return self.product.current_price * self.quantity
        return Decimal("0")
    
    def __repr__(self) -> str:
        return f"<CartItem {self.product_id} x {self.quantity}>"

