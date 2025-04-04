from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from db.base import Base
from db.base import Base
from sqlalchemy import ForeignKey

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] 