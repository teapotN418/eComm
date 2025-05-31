from pydantic import BaseModel, Field

class Item(BaseModel):
    product_id: int = Field(ge=1, default=1)
    quantity: int = Field(ge=1, default=1)

class Cart(BaseModel):
    items: list[Item] = []