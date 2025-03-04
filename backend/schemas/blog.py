from pydantic import BaseModel
import datetime

class SBlog(BaseModel):
    id: int
    tittle: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class SBlogCreate(BaseModel):
    tittle: str
    information: str

class SBlogUpdate(BaseModel):
    tittle: str
    information: str


    