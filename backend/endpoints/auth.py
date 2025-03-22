from fastapi import APIRouter, HTTPException, status,Response, Depends
from schemas.token import Token
from core.security import create_acces_token, authenticate_user, create_refresh_token, decode_acces_token
from schemas.user import SUserLogin
from db.base import redis_session
from repository.user import UserRepository
from core.config import settings

router = APIRouter()
@router.post("/login", response_model=Token)
async def login(users: SUserLogin, response: Response):
    user = await authenticate_user(email=users.email, password=users.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    user_id = await UserRepository.get_by_email(email_=users.email)
     
    access_token = create_acces_token({"sub": users.email})
    response.set_cookie(key="access_jwt_token", value=acces_token, httponly=True)
    refresh_token = create_refresh_token({"sub": users.email})
    client = redis_session
    client.hset(f"user:{user_id}", "refresh_token", refresh_token)
    client.expire(f"user:{user_id}", 604800)
    
    stored_refresh_token =client.hget(f"user:{user_id}", "refresh_token")
    if stored_refresh_token:
        print(stored_refresh_token.decode('utf-8')) 
    else:
        print("Refresh token not found or expired")
    
    return Token(
        access_token= access_token,
        token_type="Bearer")

@router.post("/refresh", response_model=Token)
async def refresh():
    client = redis_session
    stored_refresh_token = client.hget(f"user:{current_user.id}", "refresh_token")
    if stored_refresh_token:
        new_access_token = create_acces_token({"sub": current_user.email})
        return Token(
            access_token= new_access_token,
            token_type="Bearer"            
        )
    else:
        print("Refresh token not found or expired")
    