"""
Catalog Service - Business Logic for Categories and Products
"""

from typing import Optional, List
from decimal import Decimal
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from catalog.models import Category, Product
from catalog.schemas import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate
from core.exceptions import NotFoundException, ConflictException


class CategoryService:
    """Category business logic"""
    
    @staticmethod
    async def get_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        result = await db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
        """Get category by slug"""
        result = await db.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        is_active: Optional[bool] = None
    ) -> tuple[List[Category], int]:
        """Get all categories with product count"""
        query = select(Category)
        
        if is_active is not None:
            query = query.where(Category.is_active == is_active)
        
        query = query.order_by(Category.sort_order, Category.name)
        result = await db.execute(query)
        categories = result.scalars().all()
        
        # Get product counts
        for category in categories:
            count_result = await db.execute(
                select(func.count(Product.id))
                .where(Product.category_id == category.id)
            )
            category.product_count = count_result.scalar() or 0
        
        return list(categories), len(categories)
    
    @staticmethod
    async def create(db: AsyncSession, data: CategoryCreate) -> Category:
        """Create a new category"""
        # Check slug uniqueness
        existing = await CategoryService.get_by_slug(db, data.slug)
        if existing:
            raise ConflictException(detail="Category slug already exists")
        
        category = Category(**data.model_dump())
        db.add(category)
        await db.commit()
        await db.refresh(category)
        category.product_count = 0
        return category
    
    @staticmethod
    async def update(db: AsyncSession, category_id: int, data: CategoryUpdate) -> Category:
        """Update a category"""
        category = await CategoryService.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(detail="Category not found")
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Check slug uniqueness if changing
        if "slug" in update_data and update_data["slug"] != category.slug:
            existing = await CategoryService.get_by_slug(db, update_data["slug"])
            if existing:
                raise ConflictException(detail="Category slug already exists")
        
        for field, value in update_data.items():
            setattr(category, field, value)
        
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def delete(db: AsyncSession, category_id: int) -> bool:
        """Delete a category"""
        category = await CategoryService.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(detail="Category not found")
        
        await db.delete(category)
        await db.commit()
        return True


class ProductService:
    """Product business logic"""
    
    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
        """Get product by ID with relationships"""
        result = await db.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_sku(db: AsyncSession, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        result = await db.execute(
            select(Product).where(Product.sku == sku)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = True,
        search: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
    ) -> tuple[List[Product], int]:
        """Get products with pagination and filters"""
        query = select(Product).options(selectinload(Product.category))
        count_query = select(func.count(Product.id))
        
        # Apply filters
        if category_id:
            query = query.where(Product.category_id == category_id)
            count_query = count_query.where(Product.category_id == category_id)
        
        if is_active is not None:
            query = query.where(Product.is_active == is_active)
            count_query = count_query.where(Product.is_active == is_active)
        
        if search:
            search_filter = or_(
                Product.name.ilike(f"%{search}%"),
                Product.sku.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        if min_price is not None:
            query = query.where(Product.base_price >= min_price)
            count_query = count_query.where(Product.base_price >= min_price)
        
        if max_price is not None:
            query = query.where(Product.base_price <= max_price)
            count_query = count_query.where(Product.base_price <= max_price)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Product.id)
        result = await db.execute(query)
        products = result.scalars().all()
        
        # Add calculated fields
        for product in products:
            product.category_name = product.category.name if product.category else None
            product.available_stock = await ProductService.get_available_stock(db, product.id)
        
        return list(products), total
    
    @staticmethod
    async def get_available_stock(db: AsyncSession, product_id: int) -> int:
        """Get available stock for a product (sum of all batches)"""
        from inventory.models import InventoryBatch
        from datetime import date
        
        result = await db.execute(
            select(func.coalesce(
                func.sum(InventoryBatch.quantity_on_hand - InventoryBatch.quantity_reserved),
                0
            ))
            .where(
                InventoryBatch.product_id == product_id,
                or_(
                    InventoryBatch.expiry_date.is_(None),
                    InventoryBatch.expiry_date > date.today()
                )
            )
        )
        return result.scalar() or 0
    
    @staticmethod
    async def create(db: AsyncSession, data: ProductCreate) -> Product:
        """Create a new product"""
        # Check SKU uniqueness
        existing = await ProductService.get_by_sku(db, data.sku)
        if existing:
            raise ConflictException(detail="Product SKU already exists")
        
        product = Product(**data.model_dump())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        
        product.category_name = None
        product.available_stock = 0
        if product.category_id:
            category = await CategoryService.get_by_id(db, product.category_id)
            product.category_name = category.name if category else None
        
        return product
    
    @staticmethod
    async def update(db: AsyncSession, product_id: int, data: ProductUpdate) -> Product:
        """Update a product"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            raise NotFoundException(detail="Product not found")
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Check SKU uniqueness if changing
        if "sku" in update_data and update_data["sku"] != product.sku:
            existing = await ProductService.get_by_sku(db, update_data["sku"])
            if existing:
                raise ConflictException(detail="Product SKU already exists")
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        await db.commit()
        await db.refresh(product)
        
        product.category_name = product.category.name if product.category else None
        product.available_stock = await ProductService.get_available_stock(db, product.id)
        
        return product
    
    @staticmethod
    async def delete(db: AsyncSession, product_id: int) -> bool:
        """Soft delete a product (set is_active=False)"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            raise NotFoundException(detail="Product not found")
        
        product.is_active = False
        await db.commit()
        return True
    
    @staticmethod
    async def update_image(db: AsyncSession, product_id: int, image_path: str) -> Product:
        """Update product image path"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            raise NotFoundException(detail="Product not found")
        
        product.image_path = image_path
        await db.commit()
        await db.refresh(product)
        return product

