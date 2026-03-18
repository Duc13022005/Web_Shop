"""
Models Registry - Import all models to resolve SQLAlchemy relationships
"""

# Import all models here so SQLAlchemy can resolve string references in relationships
from users.models import User, UserRole, Employee, EmployeeRole
from catalog.models import Category, Product
from inventory.models import InventoryBatch
from orders.models import Order, OrderItem, Cart, CartItem, OrderStatus, PaymentMethod, PaymentStatus

# Export all models
__all__ = [
    "User",
    "UserRole",
    "Employee",
    "EmployeeRole",
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

