from pydantic import BaseModel
from typing import Optional


class Likes(BaseModel):
    blog_id: Optional[int] = None
    comment_id: Optional[int] = None
    