"""
Catalog Pydantic Schemas
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


# =====================================================
# Category Schemas
# =====================================================

class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class CategoryResponse(CategoryBase):
    """Schema for category response"""
    id: int
    image_path: Optional[str] = None
    created_at: datetime
    product_count: int = 0
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for category list"""
    items: List[CategoryResponse]
    total: int


# =====================================================
# Product Schemas
# =====================================================

class ProductBase(BaseModel):
    """Base product schema"""
    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None
    base_price: Decimal = Field(..., ge=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    unit: str = Field(default="cái", max_length=50)
    is_active: bool = True
    is_age_restricted: bool = False
    min_age: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: Optional[int] = None
    base_price: Optional[Decimal] = Field(None, ge=0)
    sale_price: Optional[Decimal] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_age_restricted: Optional[bool] = None
    min_age: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    image_path: Optional[str] = None
    current_price: Decimal
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    available_stock: int = 0
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""
    items: List[ProductResponse]
    total: int
    page: int
    size: int


class ProductSearchParams(BaseModel):
    """Search parameters for products"""
    q: Optional[str] = None  # Search query
    category_id: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    is_active: Optional[bool] = True
    in_stock: Optional[bool] = None
