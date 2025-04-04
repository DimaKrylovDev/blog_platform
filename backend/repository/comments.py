from repository.base import BaseRepository
from db.models.comments import Comments
from schemas.comments import SComment

class CommentRepository(BaseRepository):
    model=Comments
    model_pydantic_schema=SComment