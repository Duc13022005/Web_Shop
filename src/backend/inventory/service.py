"""
Inventory Service - Business Logic with FEFO and Pessimistic Locking
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from inventory.models import InventoryBatch
from inventory.schemas import (
    InventoryBatchCreate, 
    InventoryBatchUpdate, 
    InventoryAllocation,
    AllocationResult,
    LowStockItem,
    ExpiringBatchItem,
)
from catalog.models import Product
from core.exceptions import NotFoundException, InsufficientStockError, BadRequestException


class InventoryService:
    """Inventory business logic with FEFO and locking"""
    
    # =====================================================
    # Basic CRUD Operations
    # =====================================================
    
    @staticmethod
    async def get_by_id(db: AsyncSession, batch_id: int) -> Optional[InventoryBatch]:
        """Get batch by ID"""
        result = await db.execute(
            select(InventoryBatch)
            .options(selectinload(InventoryBatch.product))
            .where(InventoryBatch.id == batch_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        product_id: Optional[int] = None,
        expired: Optional[bool] = None,
        expiring_days: Optional[int] = None,
    ) -> tuple[List[InventoryBatch], int]:
        """Get batches with pagination and filters"""
        query = select(InventoryBatch).options(selectinload(InventoryBatch.product))
        count_query = select(func.count(InventoryBatch.id))
        
        # Filter by product
        if product_id:
            query = query.where(InventoryBatch.product_id == product_id)
            count_query = count_query.where(InventoryBatch.product_id == product_id)
        
        # Filter expired
        if expired is not None:
            if expired:
                query = query.where(InventoryBatch.expiry_date < date.today())
                count_query = count_query.where(InventoryBatch.expiry_date < date.today())
            else:
                query = query.where(
                    or_(
                        InventoryBatch.expiry_date.is_(None),
                        InventoryBatch.expiry_date >= date.today()
                    )
                )
                count_query = count_query.where(
                    or_(
                        InventoryBatch.expiry_date.is_(None),
                        InventoryBatch.expiry_date >= date.today()
                    )
                )
        
        # Filter expiring soon
        if expiring_days is not None:
            expiry_threshold = date.today() + timedelta(days=expiring_days)
            query = query.where(
                InventoryBatch.expiry_date.isnot(None),
                InventoryBatch.expiry_date <= expiry_threshold,
                InventoryBatch.expiry_date >= date.today()
            )
            count_query = count_query.where(
                InventoryBatch.expiry_date.isnot(None),
                InventoryBatch.expiry_date <= expiry_threshold,
                InventoryBatch.expiry_date >= date.today()
            )
        
        # Get total
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get results sorted by FEFO (expiry_date ASC)
        query = query.order_by(
            InventoryBatch.expiry_date.asc().nullslast(),
            InventoryBatch.id
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        batches = result.scalars().all()
        
        # Add product info
        for batch in batches:
            batch.product_name = batch.product.name if batch.product else None
            batch.product_sku = batch.product.sku if batch.product else None
        
        return list(batches), total
    
    @staticmethod
    async def create(db: AsyncSession, data: InventoryBatchCreate) -> InventoryBatch:
        """Create a new batch"""
        # Verify product exists
        product_result = await db.execute(
            select(Product).where(Product.id == data.product_id)
        )
        product = product_result.scalar_one_or_none()
        if not product:
            raise NotFoundException(detail="Product not found")
        
        batch = InventoryBatch(**data.model_dump())
        db.add(batch)
        await db.commit()
        await db.refresh(batch)
        
        batch.product_name = product.name
        batch.product_sku = product.sku
        
        return batch
    
    @staticmethod
    async def update(db: AsyncSession, batch_id: int, data: InventoryBatchUpdate) -> InventoryBatch:
        """Update a batch"""
        batch = await InventoryService.get_by_id(db, batch_id)
        if not batch:
            raise NotFoundException(detail="Batch not found")
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Validate quantity_reserved <= quantity_on_hand
        new_on_hand = update_data.get("quantity_on_hand", batch.quantity_on_hand)
        new_reserved = update_data.get("quantity_reserved", batch.quantity_reserved)
        if new_reserved > new_on_hand:
            raise BadRequestException(detail="Reserved quantity cannot exceed on-hand quantity")
        
        for field, value in update_data.items():
            setattr(batch, field, value)
        
        await db.commit()
        await db.refresh(batch)
        
        batch.product_name = batch.product.name if batch.product else None
        batch.product_sku = batch.product.sku if batch.product else None
        
        return batch
    
    # =====================================================
    # FEFO Allocation with Pessimistic Locking
    # =====================================================
    
    @staticmethod
    async def allocate_stock_fefo(
        db: AsyncSession,
        product_id: int,
        quantity: int
    ) -> AllocationResult:
        """
        Allocate stock using FEFO (First Expired First Out) with pessimistic locking.
        
        Uses SELECT ... FOR UPDATE to prevent race conditions.
        
        Args:
            db: Database session (must be in a transaction)
            product_id: Product to allocate
            quantity: Quantity to allocate
            
        Returns:
            AllocationResult with batch allocations
            
        Raises:
            InsufficientStockError: If not enough stock available
        """
        # Lock rows for this product - other transactions will WAIT
        query = (
            select(InventoryBatch)
            .where(
                InventoryBatch.product_id == product_id,
                InventoryBatch.quantity_on_hand > InventoryBatch.quantity_reserved,
                or_(
                    InventoryBatch.expiry_date.is_(None),
                    InventoryBatch.expiry_date > date.today()
                )
            )
            .order_by(InventoryBatch.expiry_date.asc().nullslast())  # FEFO
            .with_for_update()  # 🔒 PESSIMISTIC LOCK
        )
        
        result = await db.execute(query)
        batches = result.scalars().all()
        
        allocations: List[InventoryAllocation] = []
        remaining = quantity
        allocated_total = 0
        
        for batch in batches:
            if remaining <= 0:
                break
            
            available = batch.quantity_on_hand - batch.quantity_reserved
            allocate_qty = min(available, remaining)
            
            if allocate_qty > 0:
                # Reserve the stock
                batch.quantity_reserved += allocate_qty
                remaining -= allocate_qty
                allocated_total += allocate_qty
                
                allocations.append(InventoryAllocation(
                    batch_id=batch.id,
                    quantity=allocate_qty
                ))
        
        if remaining > 0:
            # Not enough stock - rollback will happen
            return AllocationResult(
                product_id=product_id,
                requested_quantity=quantity,
                allocated_quantity=allocated_total,
                allocations=[],
                success=False,
                message=f"Insufficient stock. Needed: {quantity}, Available: {quantity - remaining}"
            )
        
        return AllocationResult(
            product_id=product_id,
            requested_quantity=quantity,
            allocated_quantity=allocated_total,
            allocations=allocations,
            success=True,
            message="Stock allocated successfully"
        )
    
    @staticmethod
    async def release_stock(
        db: AsyncSession,
        allocations: List[InventoryAllocation]
    ) -> bool:
        """
        Release reserved stock (e.g., when order is cancelled).
        
        Args:
            db: Database session
            allocations: List of allocations to release
            
        Returns:
            True if successful
        """
        for alloc in allocations:
            batch = await InventoryService.get_by_id(db, alloc.batch_id)
            if batch:
                batch.quantity_reserved = max(0, batch.quantity_reserved - alloc.quantity)
        
        await db.commit()
        return True
    
    @staticmethod
    async def confirm_stock(
        db: AsyncSession,
        allocations: List[InventoryAllocation]
    ) -> bool:
        """
        Confirm stock allocation (reduce on_hand after shipping).
        
        Args:
            db: Database session
            allocations: List of allocations to confirm
            
        Returns:
            True if successful
        """
        for alloc in allocations:
            batch = await InventoryService.get_by_id(db, alloc.batch_id)
            if batch:
                batch.quantity_on_hand -= alloc.quantity
                batch.quantity_reserved -= alloc.quantity
        
        await db.commit()
        return True
    
    # =====================================================
    # Reports and Alerts
    # =====================================================
    
    @staticmethod
    async def get_low_stock_products(
        db: AsyncSession,
        threshold: int = 10
    ) -> List[LowStockItem]:
        """Get products with stock below threshold"""
        # Subquery for available stock per product
        subquery = (
            select(
                InventoryBatch.product_id,
                func.sum(InventoryBatch.quantity_on_hand - InventoryBatch.quantity_reserved).label("available")
            )
            .where(
                or_(
                    InventoryBatch.expiry_date.is_(None),
                    InventoryBatch.expiry_date > date.today()
                )
            )
            .group_by(InventoryBatch.product_id)
            .subquery()
        )
        
        query = (
            select(Product, subquery.c.available)
            .outerjoin(subquery, Product.id == subquery.c.product_id)
            .where(
                Product.is_active == True,
                or_(
                    subquery.c.available.is_(None),
                    subquery.c.available < threshold
                )
            )
            .order_by(subquery.c.available.asc().nullsfirst())
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        items = []
        for product, available in rows:
            # Get category name
            from catalog.models import Category
            category_name = None
            if product.category_id:
                cat_result = await db.execute(
                    select(Category.name).where(Category.id == product.category_id)
                )
                category_name = cat_result.scalar()
            
            items.append(LowStockItem(
                product_id=product.id,
                product_sku=product.sku,
                product_name=product.name,
                available_stock=available or 0,
                category_name=category_name
            ))
        
        return items
    
    @staticmethod
    async def get_expiring_batches(
        db: AsyncSession,
        days: int = 7
    ) -> List[ExpiringBatchItem]:
        """Get batches expiring within specified days"""
        expiry_threshold = date.today() + timedelta(days=days)
        
        query = (
            select(InventoryBatch)
            .options(selectinload(InventoryBatch.product))
            .where(
                InventoryBatch.expiry_date.isnot(None),
                InventoryBatch.expiry_date <= expiry_threshold,
                InventoryBatch.expiry_date >= date.today(),
                InventoryBatch.quantity_on_hand > InventoryBatch.quantity_reserved
            )
            .order_by(InventoryBatch.expiry_date.asc())
        )
        
        result = await db.execute(query)
        batches = result.scalars().all()
        
        items = []
        for batch in batches:
            items.append(ExpiringBatchItem(
                batch_id=batch.id,
                batch_code=batch.batch_code,
                product_id=batch.product_id,
                product_sku=batch.product.sku,
                product_name=batch.product.name,
                expiry_date=batch.expiry_date,
                days_until_expiry=batch.days_until_expiry or 0,
                available_quantity=batch.available_quantity,
                location=batch.location
            ))
        
        return items
    
    @staticmethod
    async def get_overview(db: AsyncSession) -> dict:
        """Get inventory overview statistics"""
        # Total products with stock
        products_result = await db.execute(
            select(func.count(func.distinct(InventoryBatch.product_id)))
        )
        total_products = products_result.scalar() or 0
        
        # Total batches
        batches_result = await db.execute(
            select(func.count(InventoryBatch.id))
        )
        total_batches = batches_result.scalar() or 0
        
        # Total stock value
        value_result = await db.execute(
            select(func.sum(
                InventoryBatch.quantity_on_hand * InventoryBatch.cost_price
            ))
        )
        total_value = value_result.scalar() or Decimal("0")
        
        # Low stock count
        low_stock = await InventoryService.get_low_stock_products(db, threshold=10)
        
        # Expiring soon count
        expiring = await InventoryService.get_expiring_batches(db, days=7)
        
        return {
            "total_products": total_products,
            "total_batches": total_batches,
            "total_stock_value": total_value,
            "low_stock_count": len(low_stock),
            "expiring_soon_count": len(expiring)
        }

