from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, String, DateTime, Enum as SQLEnum
from typing import Annotated
from datetime import datetime, timezone

from src.app.db.setup import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class OrdersORM(Base):
    __tablename__ = 'orders'
    
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(nullable=False)
    order_dict: Mapped[dict] = mapped_column(JSON(none_as_null=True), nullable=False)
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
    