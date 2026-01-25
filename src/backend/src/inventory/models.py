"""
Inventory SQLAlchemy Model - Inventory Batch (FEFO)
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.catalog.models import Product
    from src.orders.models import OrderItem


class InventoryBatch(Base):
    """Inventory Batch model for FEFO (First Expired First Out)"""
    __tablename__ = "inventory_batches"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    batch_code: Mapped[str] = mapped_column(String(50))
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    quantity_on_hand: Mapped[int] = mapped_column(Integer, default=0)
    quantity_reserved: Mapped[int] = mapped_column(Integer, default=0)
    cost_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    received_date: Mapped[date] = mapped_column(Date, default=date.today)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="inventory_batches")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="batch")
    
    @property
    def available_quantity(self) -> int:
        """Get available quantity (on_hand - reserved)"""
        return max(0, self.quantity_on_hand - self.quantity_reserved)
    
    @property
    def is_expired(self) -> bool:
        """Check if batch is expired"""
        if self.expiry_date is None:
            return False
        return self.expiry_date < date.today()
    
    @property
    def days_until_expiry(self) -> Optional[int]:
        """Days until expiry (negative if expired)"""
        if self.expiry_date is None:
            return None
        return (self.expiry_date - date.today()).days
    
    def __repr__(self) -> str:
        return f"<InventoryBatch {self.batch_code} - {self.available_quantity} available>"
