"""
Models Registry - Import all models to resolve SQLAlchemy relationships
"""

# Import all models here so SQLAlchemy can resolve string references in relationships
from src.users.models import User, UserRole
from src.catalog.models import Category, Product
from src.inventory.models import InventoryBatch
from src.orders.models import Order, OrderItem, Cart, CartItem, OrderStatus, PaymentMethod, PaymentStatus

# Export all models
__all__ = [
    "User",
    "UserRole",
    "Category",
    "Product",
    "InventoryBatch",
    "Order",
    "OrderItem",
    "Cart",
    "CartItem",
    "OrderStatus",
    "PaymentMethod",
    "PaymentStatus",
]
