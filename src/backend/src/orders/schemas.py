"""
Orders Pydantic Schemas
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from src.orders.models import OrderStatus, PaymentMethod, PaymentStatus


# =====================================================
# Cart Schemas
# =====================================================

class CartItemBase(BaseModel):
    """Base cart item schema"""
    product_id: int
    quantity: int = Field(..., ge=1)


class CartItemCreate(CartItemBase):
    """Schema for adding item to cart"""
    pass


class CartItemUpdate(BaseModel):
    """Schema for updating cart item"""
    quantity: int = Field(..., ge=1)


class CartItemResponse(CartItemBase):
    """Schema for cart item response"""
    id: int
    product_name: str
    product_sku: str
    unit_price: Decimal
    subtotal: Decimal
    image_path: Optional[str] = None
    available_stock: int = 0
    added_at: datetime
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Schema for cart response"""
    id: int
    items: List[CartItemResponse]
    total_items: int
    subtotal: Decimal
    
    class Config:
        from_attributes = True


# =====================================================
# Order Schemas
# =====================================================

class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    id: int
    product_id: int
    product_name: str
    product_sku: str
    batch_id: Optional[int] = None
    quantity: int
    price_at_purchase: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order"""
    delivery_address: str = Field(..., min_length=10)
    customer_phone: str = Field(..., min_length=10, max_length=20)
    customer_name: str = Field(..., min_length=2, max_length=100)
    notes: Optional[str] = None
    payment_method: PaymentMethod = PaymentMethod.COD
    is_age_verified: bool = False


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    status: OrderStatus
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    user_id: Optional[int]
    status: OrderStatus
    subtotal: Decimal
    delivery_fee: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    delivery_address: Optional[str]
    customer_phone: Optional[str]
    customer_name: Optional[str]
    notes: Optional[str]
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    is_age_verified: bool
    total_items: int
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for paginated order list"""
    items: List[OrderResponse]
    total: int
    page: int
    size: int


class OrderSummary(BaseModel):
    """Schema for order summary (list view)"""
    id: int
    status: OrderStatus
    total_amount: Decimal
    total_items: int
    payment_status: PaymentStatus
    customer_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
