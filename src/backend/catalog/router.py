"""
Catalog API Router - Categories and Products
"""

import os
import shutil
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.config import settings
from core.exceptions import BadRequestException
from users.models import UserRole
from auth.dependencies import get_current_user, require_roles
from catalog.schemas import (
    CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse,
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
)
from catalog.service import CategoryService, ProductService

router = APIRouter()


# =====================================================
# Category Endpoints
# =====================================================

@router.get("/categories", response_model=CategoryListResponse)
async def list_categories(
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all categories.
    
    - Public endpoint
    - Can filter by active status
    """
    categories, total = await CategoryService.get_all(db, is_active=is_active)
    return CategoryListResponse(
        items=[CategoryResponse.model_validate(c) for c in categories],
        total=total
    )


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get category by ID.
    
    - Public endpoint
    """
    from core.exceptions import NotFoundException
    category = await CategoryService.get_by_id(db, category_id)
    if not category:
        raise NotFoundException(detail="Category not found")
    
    # Add product count
    from sqlalchemy import select, func
    from catalog.models import Product
    count_result = await db.execute(
        select(func.count(Product.id)).where(Product.category_id == category_id)
    )
    category.product_count = count_result.scalar() or 0
    
    return CategoryResponse.model_validate(category)


@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Create a new category.
    
    - Requires Staff or Admin role
    """
    category = await CategoryService.create(db, data)
    return CategoryResponse.model_validate(category)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Update a category.
    
    - Requires Staff or Admin role
    """
    category = await CategoryService.update(db, category_id, data)
    return CategoryResponse.model_validate(category)


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Delete a category.
    
    - Requires Admin role
    """
    await CategoryService.delete(db, category_id)
    return {"message": "Category deleted successfully"}


# =====================================================
# Product Endpoints
# =====================================================

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    search: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List products with pagination and filters.
    
    - Public endpoint
    - Supports search, category filter, price range
    """
    skip = (page - 1) * size
    products, total = await ProductService.get_all(
        db, skip=skip, limit=size,
        category_id=category_id,
        is_active=is_active,
        search=search,
        min_price=min_price,
        max_price=max_price
    )
    
    return ProductListResponse(
        items=[ProductResponse.model_validate(p) for p in products],
        total=total,
        page=page,
        size=size
    )


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get product by ID with stock info.
    
    - Public endpoint
    """
    from core.exceptions import NotFoundException
    product = await ProductService.get_by_id(db, product_id)
    if not product:
        raise NotFoundException(detail="Product not found")
    
    product.category_name = product.category.name if product.category else None
    product.available_stock = await ProductService.get_available_stock(db, product_id)
    
    return ProductResponse.model_validate(product)


@router.post("/products", response_model=ProductResponse)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Create a new product.
    
    - Requires Staff or Admin role
    """
    product = await ProductService.create(db, data)
    return ProductResponse.model_validate(product)


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Update a product.
    
    - Requires Staff or Admin role
    """
    product = await ProductService.update(db, product_id, data)
    return ProductResponse.model_validate(product)


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Soft delete a product (set is_active=False).
    
    - Requires Admin role
    """
    await ProductService.delete(db, product_id)
    return {"message": "Product deactivated successfully"}


@router.post("/products/{product_id}/image", response_model=ProductResponse)
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Upload product image.
    
    - Requires Staff or Admin role
    - Accepts jpg, jpeg, png, webp
    - Max size: 5MB
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise BadRequestException(detail="Invalid file type. Allowed: jpg, png, webp")
    
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise BadRequestException(detail=f"File too large. Max: {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB")
    
    # Get product to find category
    product = await ProductService.get_by_id(db, product_id)
    if not product:
        from core.exceptions import NotFoundException
        raise NotFoundException(detail="Product not found")
    
    # Create upload directory
    category_slug = product.category.slug if product.category else "uncategorized"
    upload_dir = os.path.join(settings.UPLOAD_DIR, category_slug)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    ext = file.filename.split(".")[-1] if file.filename else "jpg"
    filename = f"{product.sku}.{ext}"
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Update product image path
    relative_path = f"{category_slug}/{filename}"
    product = await ProductService.update_image(db, product_id, relative_path)
    
    product.category_name = product.category.name if product.category else None
    product.available_stock = await ProductService.get_available_stock(db, product_id)
    
    return ProductResponse.model_validate(product)

