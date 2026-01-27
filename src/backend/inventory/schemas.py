"""
Inventory Pydantic Schemas
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


class InventoryBatchBase(BaseModel):
    """Base inventory batch schema"""
    product_id: int
    batch_code: str = Field(..., min_length=1, max_length=50)
    expiry_date: Optional[date] = None
    quantity_on_hand: int = Field(..., ge=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    received_date: date = Field(default_factory=date.today)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class InventoryBatchCreate(InventoryBatchBase):
    """Schema for creating an inventory batch"""
    pass


class InventoryBatchUpdate(BaseModel):
    """Schema for updating an inventory batch"""
    batch_code: Optional[str] = Field(None, min_length=1, max_length=50)
    expiry_date: Optional[date] = None
    quantity_on_hand: Optional[int] = Field(None, ge=0)
    quantity_reserved: Optional[int] = Field(None, ge=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class InventoryBatchResponse(InventoryBatchBase):
    """Schema for inventory batch response"""
    id: int
    quantity_reserved: int
    available_quantity: int
    is_expired: bool
    days_until_expiry: Optional[int]
    created_at: datetime
    product_name: Optional[str] = None
    product_sku: Optional[str] = None
    
    class Config:
        from_attributes = True


class InventoryBatchListResponse(BaseModel):
    """Schema for paginated batch list"""
    items: List[InventoryBatchResponse]
    total: int
    page: int
    size: int


class InventoryOverview(BaseModel):
    """Inventory overview schema"""
    total_products: int
    total_batches: int
    total_stock_value: Decimal
    low_stock_count: int
    expiring_soon_count: int


class LowStockItem(BaseModel):
    """Low stock item schema"""
    product_id: int
    product_sku: str
    product_name: str
    available_stock: int
    category_name: Optional[str] = None


class ExpiringBatchItem(BaseModel):
    """Expiring batch item schema"""
    batch_id: int
    batch_code: str
    product_id: int
    product_sku: str
    product_name: str
    expiry_date: date
    days_until_expiry: int
    available_quantity: int
    location: Optional[str] = None


# Allocation schemas (used in order processing)
class InventoryAllocation(BaseModel):
    """Single batch allocation"""
    batch_id: int
    quantity: int


class AllocationResult(BaseModel):
    """Result of inventory allocation"""
    product_id: int
    requested_quantity: int
    allocated_quantity: int
    allocations: List[InventoryAllocation]
    success: bool
    message: str
