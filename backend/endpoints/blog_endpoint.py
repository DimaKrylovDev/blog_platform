from fastapi import APIRouter, Depends, status
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
    blogs: BlogRepository = Depends(get_blog_repository)):
    
    await blogs.get_all(limit = limit, skip = skip)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: SBlogCreate,
    blogs: BlogRepository = Depends(get_blog_repository)):
    #user: SUser = Depends(get_current_user)):
    #
    #user_id = user.id
    
    result = await blogs.create(
        tittle = blog.tittle,
        user_id = 5,
        information = blog.information,
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
    )

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    blog: SBlogUpdate,
    blog_id: int,
    blogs: BlogRepository = Depends(get_blog_repository)):

    await blogs.update(
        id_=blog_id,
        tittle = blog.tittle,
        information = blog.information,
        updated_at = datetime.datetime.now()
    )

@router.delete("/delete")
async def delete_blog(
    blog_id: int,
    blogs: BlogRepository = Depends(get_blog_repository)):
    
    await blogs.delete(id_=blog_id)