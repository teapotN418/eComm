from pydantic import BaseModel, Field
from enum import Enum

class Status(str, Enum):
    created = "created"
    approved = "approved"
    finished = "finished"
    canceled = "canceled"

class OrderBase(BaseModel):
    user_id: int
    order_dict: dict

class OrderStatus(OrderBase):
    status: Status