from fastapi import APIRouter, HTTPException, status, Depends
from schemas.comments import SCommentCreate, SCommentUpdate
from schemas.user import SUser
from asyncpg import connect
from core.config import settings
from core.security import check_username_and_email
from .depends import get_comment_repository, get_current_user
from repository.comments import CommentRepository
import datetime
from repository.user import UserRepository

router = APIRouter()

@router.get("/read")
async def read_comments(
    skip: int = 0,
    limit: int = 100,
    comment: CommentRepository = Depends(get_comment_repository)):
    return await comment.get_all(limit=limit, skip=skip)

@router.post("/create")
async def create_comment(
    blog_id: int,
    comments: SCommentCreate,
    user: SUser = Depends(get_current_user),
    comment: CommentRepository = Depends(get_comment_repository)):
    
    await comment.create(
        user_id = user.id,
        blog_id = blog_id,
        content= comments.content,
        created_at = datetime.datetime.now(),
    )   

@router.put("/update")
async def update_comment(
    comments: SCommentUpdate,
    user_id: int,
    comment_id: int,
    current_user: SUser = Depends(get_current_user),
    comment: CommentRepository = Depends(get_comment_repository)):
    
    old_user = UserRepository.get_by_id(id_=user_id)
    if not old_user and old_user.email != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not founded")
    
    await comment.update(
        id_=comment_id,
        content=comments.content 
    )
    
@router.delete('/delete')
async def delete_comment(
    comment_id: int,
    user_id: int,
    current_user: SUser = Depends(get_current_user),
    comment:CommentRepository = Depends(get_comment_repository)):
    
    old_user = UserRepository.get_by_id(id_=user_id)
    if not old_user and old_user.email != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not founded")
    
    await comment.delete(
        id_=comment_id
    )