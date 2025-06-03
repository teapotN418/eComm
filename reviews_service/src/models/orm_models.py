from sqlalchemy.orm import mapped_column
from sqlalchemy import String, BigInteger, SmallInteger
from src.repository.db import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = mapped_column(BigInteger, primary_key=True)
    user_id = mapped_column(BigInteger)
    product_id = mapped_column(BigInteger)
    review = mapped_column(String)
    score = mapped_column(SmallInteger)
