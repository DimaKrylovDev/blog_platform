from fastapi import APIRouter, HTTPException, status,Response
from schemas.token import Token
from core.security import create_acces_token, authenticate_user
from schemas.user import SUserLogin

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(users: SUserLogin, response: Response):
    user = await authenticate_user(email=users.email, password=users.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    acces_token = create_acces_token({"sub": users.email})
    response.set_cookie(key="access_jwt_token", value=acces_token, httponly=True)
    
    return Token(
        access_token= acces_token,
        token_type="Bearer")
    
    
