from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated

from src.app.db.setup import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class UsersORM(Base):
    __tablename__ = 'users'
    
    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)