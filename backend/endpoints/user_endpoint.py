from fastapi import APIRouter, Depends, HTTPException, status, Security
from typing import List
from repository.user import UserRepository
from .depends import get_user_repository
from schemas.user import SUserRegistration, SUserUpdate
from core.security import check_username_and_email, hash_password
from sqlalchemy.exc import IntegrityError
import datetime
from asyncpg import connect
from core.config import settings
from schemas.user import SUser

router = APIRouter()

@router.get("/read")
async def read_users(
    limit: int = 100,
    skip: int = 0,
    user: UserRepository = Depends(get_user_repository)):
    result = await user.get_all(limit=limit, skip=skip)
    return result 
    
@router.post("/registration")
async def create_user(
    user: SUserRegistration,
    users: SUser = Depends(get_user_repository)):
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    role = await conn.fetch(f"SELECT id FROM roles WHERE role='user'") 
    await check_username_and_email(user.name, user.email)
    new_user = await users.create(
        role_id = dict(role[0])["id"],
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password),
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
    )
    return new_user

@router.put("/update")
async def update_user(
    user:SUserUpdate,
    user_id: int,
    users: UserRepository = Depends(get_user_repository)):
    #current_user: SUser = Depends(get_current_user)):

#    old_user = await users.get_by_id(id=user_id)
#    if old_user is None or old_user.email != current_user.email:
#        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not found user")
    
    try:
        await users.update(
            id_ = user_id,
            name = user.name,
            email = user.email,
            hashed_password = hash_password(user.password),
            updated_at = datetime.datetime.now()
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)    
    


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(  
    user_id: int,
    users: UserRepository = Depends(get_user_repository)):
    #current_user:SUser = Security(get_current_user)): 

    #old_user = await users.get_by_id(id=user_id)
    #if old_user is None and old_user.id != current_user.id:
    #    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not found user")
    
    await users.delete(
        id_=user_id
    )
    
