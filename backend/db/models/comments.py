from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from db.base import Base
import datetime
class Comments(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id", ondelete="CASCADE"))
    content: Mapped[str]
    created_at: Mapped[datetime.datetime] 
    
    user = relationship("User",back_populates="comments")
    blog = relationship("Blog",back_populates="comments")
    likes = relationship("Likes", back_populates="comment")