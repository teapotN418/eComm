from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, BigInteger, Float, ForeignKey
from src.repository.db import Base


class Providers(Base):
    __tablename__ = 'providers'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    email = mapped_column(String)
    address = mapped_column(String)

    products = relationship(
        'Product',
        back_populates='provider',
        cascade='all, delete-orphan'
    )


class Categories(Base):
    __tablename__ = 'categories'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)

    products = relationship(
        'Product',
        back_populates='category',
        cascade='all, delete-orphan'
    )


class Product(Base):
    __tablename__ = 'products'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    price = mapped_column(Float)
    description = mapped_column(String)
    minio_preview = mapped_column(String)
    provider_id = mapped_column(BigInteger, ForeignKey('providers.id'))
    category_id = mapped_column(BigInteger, ForeignKey('categories.id'))

    provider = relationship(
        'Providers',
        back_populates='products'
    )

    category = relationship(
        'Categories',
        back_populates='products'
    )
