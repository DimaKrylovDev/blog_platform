from .base import BaseRepository
from db.models.blog import Blog
from schemas.blog import SBlog

class BlogRepository(BaseRepository):
    model = Blog
    model_pydantic_schema = SBlog
        

  
    
        