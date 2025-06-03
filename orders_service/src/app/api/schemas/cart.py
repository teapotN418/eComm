from pydantic import BaseModel, Field

class Item(BaseModel):
    id: int = 1
    q: int = Field(ge=1, default=1)

class Cart(BaseModel):
    pr: list[Item] = []