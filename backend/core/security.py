from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .config import settings
from fastapi import HTTPException, status
from repository.user import UserRepository
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    jwt_encoded = jwt.encode(to_encode, settings.EE_SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update({'exp': datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), "token_type": 'refresh'})
    jwt_encoded = jwt.encode(to_encode, settings.EE_SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encoded
    
def decode_acces_token(token: str):
    try: 
        payload = jwt.decode(token, settings.EE_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.exceptions.InvalidTokenError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired or has invalid signature/format")
    
    return payload
    
#def password_match(pass2, **values):
#    if "password_1" in values and pass2 != values["password_1"]:
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Password dont match")
#    
#    return pass2

async def authenticate_user(email: EmailStr, password:str):
    user = await UserRepository.get_by_email(email_=email)
    
    if not user or not verify_password(password, user.hashed_password):
        return None
    
    return user

def get_user_email_and_role_from_token(token: str) -> tuple[int, str]:
    return(
        jwt.decode(token, settings.EE_SECRET_KEY, settings.ALGORITHM).get("sub"),
        jwt.decode(token, settings.EE_SECRET_KEY, settings.ALGORITHM).get("role")
    )

async def check_username_and_email(name: str, email:EmailStr) -> None:
    if await UserRepository.get_one_or_none(name=name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This name already taken")
    if await UserRepository.get_one_or_none(email=email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already taken")
    
