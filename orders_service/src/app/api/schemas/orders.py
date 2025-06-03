from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class Status(str, Enum):
    created = "created"
    approved = "approved"
    finished = "finished"
    canceled = "canceled"

class OrderBase(BaseModel):
    user_id: int

class OrderStatus(OrderBase):
    status: Status

class ItemOut(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    user_id: int
    status: Status
    created_at: datetime
    updated_at: datetime
    items: list[ItemOut]

    model_config = ConfigDict(from_attributes=True)