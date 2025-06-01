from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, String, DateTime, ForeignKey
from typing import Annotated
from datetime import datetime, timezone

from src.app.db.setup import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class OrdersORM(Base):
    __tablename__ = 'orders'
    
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc),
        onupdate=lambda:datetime.now(timezone.utc),
        nullable=False,
    )
    items: Mapped[list["ItemsORM"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

class ItemsORM(Base):
    __tablename__ = "items"
    
    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE")
    )
    product_id: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    order: Mapped["OrdersORM"] = relationship(back_populates="items")