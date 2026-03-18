import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, extract

from core.database import get_db
from auth.dependencies import get_current_user
from users.models import User, UserRole, Employee, EmployeeRole
from catalog.models import Product, Category
from orders.models import Order

router = APIRouter(prefix="/admin")

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires admin privileges")
    return current_user

# ─── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Dashboard statistics from real DB"""
    products_count = await db.scalar(select(func.count(Product.id)))
    users_count = await db.scalar(select(func.count(User.id)))
    orders_count = await db.scalar(select(func.count(Order.id)))
    revenue = await db.scalar(select(func.sum(Order.total_amount)))

    # Real category distribution: count products per category
    cat_result = await db.execute(
        select(Category.name, func.count(Product.id))
        .join(Product, Product.category_id == Category.id, isouter=True)
        .group_by(Category.id, Category.name)
        .limit(8)
    )
    distribution = [{"name": row[0], "value": row[1] or 0} for row in cat_result.all()]

    # Monthly orders / revenue for current year
    monthly_result = await db.execute(
        select(
            extract('month', Order.created_at).label('month'),
            func.count(Order.id).label('orders'),
            func.sum(Order.total_amount).label('revenue')
        )
        .where(extract('year', Order.created_at) == datetime.now().year)
        .group_by(extract('month', Order.created_at))
        .order_by(extract('month', Order.created_at))
    )
    month_names = ["", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]
    monthly_data = [
        {"name": month_names[int(row.month)], "orders": int(row.orders), "revenue": float(row.revenue or 0)}
        for row in monthly_result.all()
    ]

    return {
        "total_products": products_count or 0,
        "total_users": users_count or 0,
        "total_orders": orders_count or 0,
        "total_revenue": float(revenue or 0),
        "category_distribution": distribution,
        "monthly_data": monthly_data,
    }

# ─── Employees ────────────────────────────────────────────────────────────────

@router.get("/employees")
async def get_employees(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).order_by(Employee.id))
    employees = result.scalars().all()
    return [{
        "id": emp.id,
        "full_name": emp.full_name,
        "email": emp.email,
        "phone": emp.phone or "",
        "role": emp.role.value,
        "salary": emp.salary,
        "is_active": emp.is_active,
        "join_date": emp.join_date.strftime("%Y-%m-%d") if emp.join_date else None
    } for emp in employees]


@router.post("/employees")
async def create_employee(data: dict, db: AsyncSession = Depends(get_db)):
    role_map = {"Vệ sinh": EmployeeRole.cleaner, "Thu ngân": EmployeeRole.cashier, "Shipper": EmployeeRole.shipper}
    role_enum = role_map.get(data.get("role", "Thu ngân"), EmployeeRole.cashier)
    emp = Employee(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        role=role_enum,
        salary=float(data.get("salary", 0)),
        is_active=True,
    )
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return {"message": "Employee created", "id": emp.id}


@router.put("/employees/{emp_id}")
async def update_employee(emp_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).filter(Employee.id == emp_id))
    emp = result.scalars().first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    role_map = {"Vệ sinh": EmployeeRole.cleaner, "Thu ngân": EmployeeRole.cashier, "Shipper": EmployeeRole.shipper}
    if "full_name" in data: emp.full_name = data["full_name"]
    if "email" in data: emp.email = data["email"]
    if "phone" in data: emp.phone = data["phone"]
    if "salary" in data: emp.salary = float(data["salary"])
    if "is_active" in data: emp.is_active = data["is_active"]
    if "role" in data: emp.role = role_map.get(data["role"], emp.role)
    await db.commit()
    return {"message": "Employee updated"}


@router.delete("/employees/{emp_id}")
async def delete_employee(emp_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee).filter(Employee.id == emp_id))
    emp = result.scalars().first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    await db.delete(emp)
    await db.commit()
    return {"message": "Employee deleted"}

# ─── Products (Inventory) ──────────────────────────────────────────────────────

@router.get("/products")
async def get_admin_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).order_by(Product.id))
    products = result.scalars().all()
    return [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "base_price": p.base_price,
        "sale_price": p.sale_price,
        "unit": p.unit,
        "is_active": p.is_active,
    } for p in products]


@router.post("/products")
async def create_admin_product(data: dict, db: AsyncSession = Depends(get_db)):
    new_product = Product(
        sku=data.get("sku") or str(uuid.uuid4())[:8].upper(),
        name=data["name"],
        base_price=float(data["base_price"]),
        sale_price=float(data["sale_price"]) if data.get("sale_price") else None,
        unit=data.get("unit", "cái"),
        is_active=data.get("is_active", True),
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return {"message": "Product created", "id": new_product.id}


@router.put("/products/{product_id}")
async def update_admin_product(product_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if "name" in data: product.name = data["name"]
    if "base_price" in data: product.base_price = float(data["base_price"])
    if "sale_price" in data: product.sale_price = float(data["sale_price"]) if data["sale_price"] else None
    if "unit" in data: product.unit = data["unit"]
    if "is_active" in data: product.is_active = data["is_active"]
    await db.commit()
    return {"message": "Product updated"}


@router.delete("/products/{product_id}")
async def delete_admin_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted"}
