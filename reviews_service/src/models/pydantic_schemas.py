from pydantic import BaseModel, Field


class ReviewIn(BaseModel):
    user_id: int = Field(...)
    product_id: int = Field(...)
    review: str = Field(..., min_length=10, max_length=300)
    score: int = Field(..., ge=1, le=10)


class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    review: str
    score: int


class AvgScore(BaseModel):
    score: float
