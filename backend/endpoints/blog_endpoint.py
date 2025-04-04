from fastapi import APIRouter, Depends, status, HTTPException
from repository.blog import BlogRepository
from schemas.blog import SBlog, SBlogUpdate, SBlogCreate 
from .depends import get_blog_repository, get_current_user
import datetime
from repository.user import UserRepository
from schemas.user import SUser

router = APIRouter()

@router.get("/read")
async def read_blogs(
    limit: int = 100,
    skip: int = 0,
    blog: BlogRepository = Depends(get_blog_repository)):
    
    return await blog.get_all(limit=limit, skip=skip)
 
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: SBlogCreate,
    blogs: BlogRepository = Depends(get_blog_repository),
    current_user: SUser = Depends(get_current_user)):
    
    user_id = current_user.id
    
    await blogs.create(
        user_id = user_id,
        tittle = blog.tittle,
        information = blog.information,
        created_at = datetime.datetime.now(),
    )

@router.put("/update", status_code=status.HTTP_200_OK)
async def update(
    blog: SBlogUpdate,
    user_id: int,
    blog_id: int,
    current_user: SUser = Depends(get_current_user),
    blogs: BlogRepository = Depends(get_blog_repository)):

    old_user = UserRepository.get_by_id(id_=user_id)
    if old_user is None and old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    
    await blogs.update(
        id_=blog_id,
        tittle = blog.tittle,
        information = blog.information,
    )

@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_blog(
    user_id: int,
    blog_id: int,
    current_user: SUser = Depends(get_current_user),
    blogs: BlogRepository = Depends(get_blog_repository)):
    
    old_user = UserRepository.get_by_id(id_=user_id)
    if old_user is None and old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    
    await blogs.delete(id_=blog_id)