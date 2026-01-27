"""
Inventory API Router
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from users.models import UserRole
from auth.dependencies import require_roles
from inventory.schemas import (
    InventoryBatchCreate,
    InventoryBatchUpdate,
    InventoryBatchResponse,
    InventoryBatchListResponse,
    InventoryOverview,
    LowStockItem,
    ExpiringBatchItem,
)
from inventory.service import InventoryService

router = APIRouter(prefix="/inventory")


@router.get("/overview", response_model=InventoryOverview)
async def get_inventory_overview(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Get inventory overview statistics.
    
    - Requires Staff or Admin role
    """
    overview = await InventoryService.get_overview(db)
    return InventoryOverview(**overview)


@router.get("/batches", response_model=InventoryBatchListResponse)
async def list_batches(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    product_id: Optional[int] = None,
    expired: Optional[bool] = None,
    expiring_days: Optional[int] = Query(None, ge=1, description="Filter batches expiring within N days"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    List inventory batches with pagination and filters.
    
    - Requires Staff or Admin role
    - Sorted by FEFO (First Expired First Out)
    """
    skip = (page - 1) * size
    batches, total = await InventoryService.get_all(
        db, skip=skip, limit=size,
        product_id=product_id,
        expired=expired,
        expiring_days=expiring_days
    )
    
    return InventoryBatchListResponse(
        items=[InventoryBatchResponse.model_validate(b) for b in batches],
        total=total,
        page=page,
        size=size
    )


@router.get("/batches/{batch_id}", response_model=InventoryBatchResponse)
async def get_batch(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Get batch by ID.
    
    - Requires Staff or Admin role
    """
    from core.exceptions import NotFoundException
    batch = await InventoryService.get_by_id(db, batch_id)
    if not batch:
        raise NotFoundException(detail="Batch not found")
    
    batch.product_name = batch.product.name if batch.product else None
    batch.product_sku = batch.product.sku if batch.product else None
    
    return InventoryBatchResponse.model_validate(batch)


@router.post("/batches", response_model=InventoryBatchResponse)
async def create_batch(
    data: InventoryBatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Create a new inventory batch (receive stock).
    
    - Requires Admin role
    """
    batch = await InventoryService.create(db, data)
    return InventoryBatchResponse.model_validate(batch)


@router.put("/batches/{batch_id}", response_model=InventoryBatchResponse)
async def update_batch(
    batch_id: int,
    data: InventoryBatchUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin]))
):
    """
    Update an inventory batch.
    
    - Requires Admin role
    """
    batch = await InventoryService.update(db, batch_id, data)
    return InventoryBatchResponse.model_validate(batch)


@router.get("/low-stock", response_model=list[LowStockItem])
async def get_low_stock(
    threshold: int = Query(10, ge=1, description="Stock threshold"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Get products with stock below threshold.
    
    - Requires Staff or Admin role
    """
    return await InventoryService.get_low_stock_products(db, threshold=threshold)


@router.get("/expiring", response_model=list[ExpiringBatchItem])
async def get_expiring_batches(
    days: int = Query(7, ge=1, description="Days until expiry"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Get batches expiring within specified days.
    
    - Requires Staff or Admin role
    - Default: 7 days
    """
    return await InventoryService.get_expiring_batches(db, days=days)

