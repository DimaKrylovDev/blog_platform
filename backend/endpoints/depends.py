from repository.user import UserRepository 
from repository.blog import BlogRepository
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_acces_token
from jose import JWTError


def get_user_repository() -> UserRepository:
    return UserRepository()

def get_blog_repository() -> BlogRepository:
    return BlogRepository()

def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    credentional_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_acces_token(token)
        if payload is None:
            raise credentional_exeptions
        user_email = payload.get("sub")
        if user_email is None:
            raise credentional_exeptions
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    
    user = UserRepository.get_by_email(email_=user_email)
    if user is None:
        raise credentional_exeptions
    
    return user