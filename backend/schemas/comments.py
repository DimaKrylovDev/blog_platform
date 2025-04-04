from pydantic import BaseModel, EmailStr
import datetime

class SComment(BaseModel):
    id: int
    content: str
    likes: int = 0
    created_at: datetime.datetime
    
class SCommentCreate(BaseModel):
    content: str
    created_at: datetime.datetime
    
class SCommentUpdate(BaseModel):
    content:str