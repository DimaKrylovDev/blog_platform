from repository.user import UserRepository 
from repository.blog import BlogRepository
from repository.comments import CommentRepository
from repository.likes import LikeRepository
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_acces_token
from jose import JWTError



def get_user_repository() -> UserRepository:
    return UserRepository()

def get_blog_repository() -> BlogRepository:
    return BlogRepository()

def get_comment_repository() -> CommentRepository:
    return CommentRepository()

def get_like_repository() -> LikeRepository:
    return LikeRepository()

async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/login"))]):
    credentional_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_acces_token(token)
        print(payload)
        if not payload:
            raise credentional_exeptions
        username = payload.get('sub')
        print(username)
        if username is None:
            raise credentional_exeptions
        user = await UserRepository.get_one_or_none(name=username)
        print(user)
        if user is None:
            raise credentional_exeptions
    
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    

