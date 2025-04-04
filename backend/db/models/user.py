from sqlalchemy.orm import Mapped, mapped_column, relationship 
import datetime
from sqlalchemy import ForeignKey
from db.base import Base
from typing import List

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime.datetime]
    
    blogs: Mapped[List["Blog"]] = relationship(back_populates="user",uselist=True, foreign_keys="Blog.user_id")
    comments: Mapped[List["Comments"]] = relationship(back_populates="user", uselist=True, foreign_keys="Comments.user_id")
    likes: Mapped[List["Likes"]] = relationship(uselist=True, foreign_keys="Likes.user_id")