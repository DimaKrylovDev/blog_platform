from pydantic import BaseModel, EmailStr
import datetime


class SUser(BaseModel):
    id: int
    role_id: int
    email: EmailStr
    name: str
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
class SUserLogin(BaseModel):
    email: EmailStr
    password: str 

class SUserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str


class SUserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str


    
    


    
 
        