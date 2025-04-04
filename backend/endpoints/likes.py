from fastapi import APIRouter, Depends, HTTPException, status, Query
from repository.likes import LikeRepository
from .depends import get_current_user, get_like_repository
from core.security import check_username_and_email
from schemas.user import SUser
from schemas.likes import Likes
from core.config import settings 
import psycopg2
from typing import Optional

router = APIRouter()

@router.get("/read/blog_likes")
async def get_blog_likes(
    blog_id: Optional[int] = Query(None),
    like: LikeRepository = Depends(get_like_repository)):
    
    result = await like.get_blog_likes(blog_id = blog_id)
    print(result)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No likes on this entity")
    return {"count:": result}

@router.get("/read/comment_likes")
async def get_comment_likes(
    comment_id: Optional[int] = Query(None),
    like: LikeRepository = Depends(get_like_repository)):
    
    result = await like.get_comment_likes(comment_id=comment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No likes on this entity")
    return {"count:": result} 
    
@router.post("/add")
async def add_like(
    likeRequest: Likes,
    like: LikeRepository = Depends(get_like_repository),
    user: SUser = Depends(get_current_user)):
    
    conn = psycopg2.connect(settings.POSTGRES_CLEAR_URL)
    cursor = conn.cursor()
    
    if likeRequest.blog_id:
        cursor.execute(f'SELECT 1 FROM likes where user_id = {user.id} and blog_id = {likeRequest.blog_id}')
        if cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user has already like on this blog')
    elif likeRequest.comment_id:
        comment_id = cursor.execute(f'SELECT 1 FROM likes where user_id = {user.id} and comment_id = {likeRequest.comment_id}')
        if cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='user has already like on this comment')
    
    await like.create(
        user_id = user.id,
        blog_id = likeRequest.blog_id,
        comment_id = likeRequest.comment_id
    )
    
@router.delete("/delete")
async def delete_like(
    id: int,
    like: LikeRepository = Depends(get_like_repository),
    user: SUser = Depends(get_current_user)):
    
   await like.delete(id_=id)
