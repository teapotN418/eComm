from pydantic import BaseModel, EmailStr


class CategoryOut(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ProviderOut(BaseModel):
    name: str
    email: EmailStr
    address: str

    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    name: str
    price: float
    description: str
    minio_preview: str
    provider: ProviderOut
    category: CategoryOut

    class Config:
        orm_mode = True
