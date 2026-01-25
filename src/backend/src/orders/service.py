"""
Orders Service - Business Logic for Cart and Orders
"""

from decimal import Decimal
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.orders.models import Order, OrderItem, OrderStatus, Cart, CartItem
from src.orders.schemas import OrderCreate, OrderStatusUpdate
from src.catalog.models import Product
from src.catalog.service import ProductService
from src.inventory.service import InventoryService
from src.inventory.schemas import InventoryAllocation
from src.users.models import User
from src.core.exceptions import (
    NotFoundException, 
    BadRequestException, 
    InsufficientStockError,
    AgeRestrictionError,
    ForbiddenException,
)


class CartService:
    """Shopping cart business logic"""
    
    @staticmethod
    async def get_or_create_cart(db: AsyncSession, user_id: int) -> Cart:
        """Get user's cart or create if not exists"""
        result = await db.execute(
            select(Cart)
            .options(
                selectinload(Cart.items).selectinload(CartItem.product)
            )
            .where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
            cart.items = []
        
        return cart
    
    @staticmethod
    async def add_item(db: AsyncSession, user_id: int, product_id: int, quantity: int) -> Cart:
        """Add item to cart or update quantity if exists"""
        # Verify product exists and is active
        product = await ProductService.get_by_id(db, product_id)
        if not product or not product.is_active:
            raise NotFoundException(detail="Product not found or inactive")
        
        # Check available stock
        available = await ProductService.get_available_stock(db, product_id)
        if available < quantity:
            raise InsufficientStockError(detail=f"Only {available} items available")
        
        cart = await CartService.get_or_create_cart(db, user_id)
        
        # Check if item already in cart
        existing_item = None
        for item in cart.items:
            if item.product_id == product_id:
                existing_item = item
                break
        
        if existing_item:
            new_qty = existing_item.quantity + quantity
            if new_qty > available:
                raise InsufficientStockError(detail=f"Only {available} items available")
            existing_item.quantity = new_qty
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.add(cart_item)
        
        await db.commit()
        return await CartService.get_or_create_cart(db, user_id)
    
    @staticmethod
    async def update_item(db: AsyncSession, user_id: int, item_id: int, quantity: int) -> Cart:
        """Update cart item quantity"""
        cart = await CartService.get_or_create_cart(db, user_id)
        
        # Find item
        item = None
        for cart_item in cart.items:
            if cart_item.id == item_id:
                item = cart_item
                break
        
        if not item:
            raise NotFoundException(detail="Cart item not found")
        
        # Check available stock
        available = await ProductService.get_available_stock(db, item.product_id)
        if quantity > available:
            raise InsufficientStockError(detail=f"Only {available} items available")
        
        item.quantity = quantity
        await db.commit()
        
        return await CartService.get_or_create_cart(db, user_id)
    
    @staticmethod
    async def remove_item(db: AsyncSession, user_id: int, item_id: int) -> Cart:
        """Remove item from cart"""
        cart = await CartService.get_or_create_cart(db, user_id)
        
        # Find and remove item
        for cart_item in cart.items:
            if cart_item.id == item_id:
                await db.delete(cart_item)
                break
        else:
            raise NotFoundException(detail="Cart item not found")
        
        await db.commit()
        return await CartService.get_or_create_cart(db, user_id)
    
    @staticmethod
    async def clear_cart(db: AsyncSession, user_id: int) -> bool:
        """Clear all items from cart"""
        cart = await CartService.get_or_create_cart(db, user_id)
        
        for item in cart.items:
            await db.delete(item)
        
        await db.commit()
        return True


class OrderService:
    """Order business logic"""
    
    DELIVERY_FEE = Decimal("15000")  # 15,000 VND flat rate
    
    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: int) -> Optional[Order]:
        """Get order by ID with items"""
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.user)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_orders(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[OrderStatus] = None
    ) -> tuple[List[Order], int]:
        """Get orders for a user"""
        query = select(Order).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        ).where(Order.user_id == user_id)
        count_query = select(func.count(Order.id)).where(Order.user_id == user_id)
        
        if status:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)
        
        # Get total
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get orders
        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        orders = result.scalars().all()
        
        return list(orders), total
    
    @staticmethod
    async def get_all_orders(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        status: Optional[OrderStatus] = None
    ) -> tuple[List[Order], int]:
        """Get all orders (admin/staff)"""
        query = select(Order).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
        count_query = select(func.count(Order.id))
        
        if status:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)
        
        # Get total
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Get orders
        query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        orders = result.scalars().all()
        
        return list(orders), total
    
    @staticmethod
    async def create_from_cart(db: AsyncSession, user: User, data: OrderCreate) -> Order:
        """
        Create order from user's cart.
        
        This is the main order creation flow:
        1. Validate cart has items
        2. Check age restriction if needed
        3. Reserve inventory using FEFO with locking
        4. Create order and order items
        5. Clear cart
        """
        # Get cart with items
        cart = await CartService.get_or_create_cart(db, user.id)
        
        if not cart.items:
            raise BadRequestException(detail="Cart is empty")
        
        # Check for age-restricted products
        has_restricted = False
        for item in cart.items:
            if item.product.is_age_restricted:
                has_restricted = True
                break
        
        if has_restricted and not data.is_age_verified:
            raise AgeRestrictionError(detail="Age verification required for restricted products")
        
        # Start transaction for stock allocation
        async with db.begin_nested():
            # Allocate stock for each item using FEFO with locking
            all_allocations: List[tuple[int, int, Decimal, List[InventoryAllocation]]] = []
            
            for item in cart.items:
                allocation_result = await InventoryService.allocate_stock_fefo(
                    db, item.product_id, item.quantity
                )
                
                if not allocation_result.success:
                    # Rollback will happen automatically
                    raise InsufficientStockError(
                        detail=f"Insufficient stock for {item.product.name}: {allocation_result.message}"
                    )
                
                all_allocations.append((
                    item.product_id,
                    item.quantity,
                    item.product.current_price,
                    allocation_result.allocations
                ))
            
            # Calculate totals
            subtotal = sum(
                qty * price for _, qty, price, _ in all_allocations
            )
            total_amount = subtotal + OrderService.DELIVERY_FEE
            
            # Create order
            order = Order(
                user_id=user.id,
                status=OrderStatus.PENDING,
                subtotal=subtotal,
                delivery_fee=OrderService.DELIVERY_FEE,
                discount_amount=Decimal("0"),
                total_amount=total_amount,
                delivery_address=data.delivery_address,
                customer_phone=data.customer_phone,
                customer_name=data.customer_name,
                notes=data.notes,
                payment_method=data.payment_method,
                is_age_verified=data.is_age_verified,
            )
            db.add(order)
            await db.flush()  # Get order.id
            
            # Create order items
            for product_id, quantity, price, allocations in all_allocations:
                # Create one order item per allocation (batch)
                for alloc in allocations:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product_id,
                        batch_id=alloc.batch_id,
                        quantity=alloc.quantity,
                        price_at_purchase=price,
                        subtotal=price * alloc.quantity
                    )
                    db.add(order_item)
            
            # Clear cart
            for item in cart.items:
                await db.delete(item)
        
        await db.commit()
        
        # Refresh and return
        return await OrderService.get_by_id(db, order.id)
    
    @staticmethod
    async def update_status(
        db: AsyncSession, 
        order_id: int, 
        data: OrderStatusUpdate,
        user: User
    ) -> Order:
        """Update order status"""
        order = await OrderService.get_by_id(db, order_id)
        if not order:
            raise NotFoundException(detail="Order not found")
        
        old_status = order.status
        new_status = data.status
        
        # Validate status transitions
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PICKING, OrderStatus.CANCELLED],
            OrderStatus.PICKING: [OrderStatus.DELIVERING, OrderStatus.CANCELLED],
            OrderStatus.DELIVERING: [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
            OrderStatus.COMPLETED: [],
            OrderStatus.CANCELLED: [],
        }
        
        if new_status not in valid_transitions.get(old_status, []):
            raise BadRequestException(
                detail=f"Cannot transition from {old_status.value} to {new_status.value}"
            )
        
        order.status = new_status
        if data.notes:
            order.notes = (order.notes or "") + f"\n[{new_status.value}] {data.notes}"
        
        # Handle cancellation - release stock
        if new_status == OrderStatus.CANCELLED:
            allocations = [
                InventoryAllocation(batch_id=item.batch_id, quantity=item.quantity)
                for item in order.items
                if item.batch_id
            ]
            await InventoryService.release_stock(db, allocations)
        
        # Handle completion - confirm stock reduction
        if new_status == OrderStatus.COMPLETED:
            allocations = [
                InventoryAllocation(batch_id=item.batch_id, quantity=item.quantity)
                for item in order.items
                if item.batch_id
            ]
            await InventoryService.confirm_stock(db, allocations)
            order.payment_status = "paid"
        
        await db.commit()
        return await OrderService.get_by_id(db, order_id)
    
    @staticmethod
    async def cancel_order(db: AsyncSession, order_id: int, user: User) -> Order:
        """Cancel an order (customer can cancel if pending)"""
        order = await OrderService.get_by_id(db, order_id)
        if not order:
            raise NotFoundException(detail="Order not found")
        
        # Check ownership for customers
        from src.users.models import UserRole
        if user.role == UserRole.customer and order.user_id != user.id:
            raise ForbiddenException(detail="Cannot cancel other user's order")
        
        # Only pending orders can be cancelled by customer
        if user.role == UserRole.customer and order.status != OrderStatus.PENDING:
            raise BadRequestException(
                detail="Only pending orders can be cancelled"
            )
        
        # Cancel
        return await OrderService.update_status(
            db, order_id,
            OrderStatusUpdate(status=OrderStatus.CANCELLED, notes="Cancelled by user"),
            user
        )
