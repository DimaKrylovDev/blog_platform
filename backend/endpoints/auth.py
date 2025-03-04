from fastapi import APIRouter, Depends, HTTPException, status
from repository.user import UserRepository
from schemas.token import Token
from .depends import get_user_repository
from core.security import verify_password, create_acces_token, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    return Token(
        access_token= create_acces_token({"sub": user.email}),
        token_type="Bearer")
