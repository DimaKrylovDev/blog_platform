from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from schemas.token import Token
from core.security import create_acces_token, authenticate_user, create_refresh_token, decode_acces_token
from schemas.user import SUser
from db.base import redis_session
from repository.user import UserRepository
from core.config import settings
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from .depends import get_current_user

router = APIRouter()
@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    user = await authenticate_user(username=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
     
    access_token = create_acces_token({"sub": user.name})
    response.set_cookie(key="access_jwt_token", value=access_token, httponly=True)
    refresh_token = create_refresh_token({"sub": user.email})
    client = redis_session
    client.hset(f"user:{user.id}", "refresh_token", refresh_token)
    client.expire(f"user:{user.id}", 604800)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    
    stored_refresh_token = client.hget(f"user:{user.id}", "refresh_token")
    if stored_refresh_token:
        print(stored_refresh_token.decode('utf-8')) 
    else:
        print("Refresh token not found or expired")
    
    return Token(
        access_token= access_token,
        token_type="Bearer")

@router.post("/refresh", response_model=Token)
async def refresh(request: Request, response: Response, current_user: SUser = Depends(get_current_user)):
    
    refresh_token = request.cookies.get('refresh_token')
    payload = decode_acces_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is unauthorized", headers={"WWW-Authenticate": "refresh"},) 
    user_email = payload.get("sub")
    current_user = UserRepository.get_by_email(email_=user_email)
    client = redis_session
    stored_refresh_token = client.hget(f"user:{current_user.id}", "refresh_token")
    if stored_refresh_token:
        new_access_token = create_acces_token({"sub": current_user.email})
        response.set_cookie(key="access_token", value=new_access_token, httponly=True)
        return Token(
            access_token= new_access_token,
            token_type="Bearer"            
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Refresh token not found or expired")
    