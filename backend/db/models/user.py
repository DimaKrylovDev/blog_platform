from sqlalchemy.orm import Mapped, mapped_column, relationship 
from uuid import UUID
import datetime
from sqlalchemy import ForeignKey
from db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime] 
    blogs: Mapped[list["Blog"]] = relationship(uselist=True)
    role: Mapped["Role"] = relationship()
    