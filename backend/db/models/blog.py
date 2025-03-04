from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import datetime
from db.base import Base

class Blog(Base):
    __tablename__ = "blogs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    tittle: Mapped[str]
    information: Mapped[str]
    created_at: Mapped[datetime.datetime] 
    updated_at: Mapped[datetime.datetime] 
    user: Mapped["User"] = relationship(back_populates="blogs")
    
