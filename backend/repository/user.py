from .base import BaseRepository
from db.models.user import User
from schemas.user import SUser


class UserRepository(BaseRepository):
    model = User
    model_pydantic_schema = SUser