from pydantic import BaseModel, EmailStr, Field


class CategoryIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProviderIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    address: str = Field(..., min_length=10, max_length=255)


class ProviderOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str

    class Config:
        orm_mode = True


class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: int = Field(...)
    description: str = Field(..., min_length=10, max_length=1024)
    minio_preview: str = Field(..., min_length=10, max_length=100)
    provider_id: int = Field(...)
    category_id: int = Field(...)


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: str
    minio_preview: str
    provider: ProviderOut
    category: CategoryOut

    class Config:
        orm_mode = True
