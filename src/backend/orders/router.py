"""
Orders API Router - Cart and Orders
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from users.models import User, UserRole
from auth.dependencies import get_current_user, require_roles
from orders.models import OrderStatus
from orders.schemas import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
    CartItemResponse,
    OrderCreate,
    OrderStatusUpdate,
    OrderResponse,
    OrderListResponse,
    OrderItemResponse,
)
from orders.service import CartService, OrderService
from catalog.service import ProductService

router = APIRouter()


# =====================================================
# Cart Endpoints
# =====================================================

@router.get("/cart", response_model=CartResponse)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's cart.
    
    - Returns cart with all items
    """
    cart = await CartService.get_or_create_cart(db, current_user.id)
    
    items = []
    for item in cart.items:
        available = await ProductService.get_available_stock(db, item.product_id)
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_sku=item.product.sku,
            unit_price=item.product.current_price,
            subtotal=item.subtotal,
            image_path=item.product.image_path,
            available_stock=available,
            added_at=item.added_at
        ))
    
    return CartResponse(
        id=cart.id,
        items=items,
        total_items=cart.total_items,
        subtotal=cart.subtotal
    )


@router.post("/cart/items", response_model=CartResponse)
async def add_to_cart(
    data: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add item to cart.
    
    - Creates cart if not exists
    - Updates quantity if item already in cart
    """
    cart = await CartService.add_item(db, current_user.id, data.product_id, data.quantity)
    
    items = []
    for item in cart.items:
        available = await ProductService.get_available_stock(db, item.product_id)
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_sku=item.product.sku,
            unit_price=item.product.current_price,
            subtotal=item.subtotal,
            image_path=item.product.image_path,
            available_stock=available,
            added_at=item.added_at
        ))
    
    return CartResponse(
        id=cart.id,
        items=items,
        total_items=cart.total_items,
        subtotal=cart.subtotal
    )


@router.put("/cart/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    data: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update cart item quantity.
    """
    cart = await CartService.update_item(db, current_user.id, item_id, data.quantity)
    
    items = []
    for item in cart.items:
        available = await ProductService.get_available_stock(db, item.product_id)
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_sku=item.product.sku,
            unit_price=item.product.current_price,
            subtotal=item.subtotal,
            image_path=item.product.image_path,
            available_stock=available,
            added_at=item.added_at
        ))
    
    return CartResponse(
        id=cart.id,
        items=items,
        total_items=cart.total_items,
        subtotal=cart.subtotal
    )


@router.delete("/cart/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove item from cart.
    """
    cart = await CartService.remove_item(db, current_user.id, item_id)
    
    items = []
    for item in cart.items:
        available = await ProductService.get_available_stock(db, item.product_id)
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name,
            product_sku=item.product.sku,
            unit_price=item.product.current_price,
            subtotal=item.subtotal,
            image_path=item.product.image_path,
            available_stock=available,
            added_at=item.added_at
        ))
    
    return CartResponse(
        id=cart.id,
        items=items,
        total_items=cart.total_items,
        subtotal=cart.subtotal
    )


@router.delete("/cart/clear")
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Clear all items from cart.
    """
    await CartService.clear_cart(db, current_user.id)
    return {"message": "Cart cleared successfully"}


# =====================================================
# Order Endpoints
# =====================================================

def _order_to_response(order) -> OrderResponse:
    """Convert order model to response"""
    items = []
    for item in order.items:
        items.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product.name if item.product else "Unknown",
            product_sku=item.product.sku if item.product else "N/A",
            batch_id=item.batch_id,
            quantity=item.quantity,
            price_at_purchase=item.price_at_purchase,
            subtotal=item.subtotal
        ))
    
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        subtotal=order.subtotal,
        delivery_fee=order.delivery_fee,
        discount_amount=order.discount_amount,
        total_amount=order.total_amount,
        delivery_address=order.delivery_address,
        customer_phone=order.customer_phone,
        customer_name=order.customer_name,
        notes=order.notes,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        is_age_verified=order.is_age_verified,
        total_items=order.total_items,
        items=items,
        created_at=order.created_at,
        updated_at=order.updated_at
    )


@router.get("/orders", response_model=OrderListResponse)
async def list_orders(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List orders.
    
    - Customers see their own orders
    - Staff/Admin see all orders
    """
    skip = (page - 1) * size
    
    if current_user.role == UserRole.customer:
        orders, total = await OrderService.get_user_orders(
            db, current_user.id, skip=skip, limit=size, status=status
        )
    else:
        orders, total = await OrderService.get_all_orders(
            db, skip=skip, limit=size, status=status
        )
    
    return OrderListResponse(
        items=[_order_to_response(o) for o in orders],
        total=total,
        page=page,
        size=size
    )


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get order by ID.
    
    - Customers can only view their own orders
    """
    from core.exceptions import NotFoundException, ForbiddenException
    
    order = await OrderService.get_by_id(db, order_id)
    if not order:
        raise NotFoundException(detail="Order not found")
    
    # Check access
    if current_user.role == UserRole.CUSTOMER and order.user_id != current_user.id:
        raise ForbiddenException(detail="Access denied")
    
    return _order_to_response(order)


@router.post("/orders", response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create order from cart.
    
    - Validates stock availability
    - Reserves inventory using FEFO
    - Clears cart after success
    """
    order = await OrderService.create_from_cart(db, current_user, data)
    return _order_to_response(order)


@router.put("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.admin, UserRole.staff]))
):
    """
    Update order status.
    
    - Requires Staff or Admin role
    - Validates status transitions
    - Handles stock release on cancellation
    """
    order = await OrderService.update_status(db, order_id, data, current_user)
    return _order_to_response(order)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel an order.
    
    - Customers can cancel pending orders
    - Staff/Admin can cancel any order
    """
    order = await OrderService.cancel_order(db, order_id, current_user)
    return _order_to_response(order)

