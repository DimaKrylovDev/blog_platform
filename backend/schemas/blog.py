from pydantic import BaseModel
from typing import List
import datetime

class SBlog(BaseModel):
    id: int
    tittle: str
    information: str
    likes:int = 0
    created_at: datetime.datetime

class SBlogCreate(BaseModel):
    tittle: str
    information: str

class SBlogUpdate(BaseModel):
    tittle: str
    information: str


    