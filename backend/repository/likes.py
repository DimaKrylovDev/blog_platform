from db.base import async_session_maker
from sqlalchemy import select, delete, insert, func
from db.models import Likes

class LikeRepository:
    model = Likes
    
    @classmethod
    async def get_blog_likes(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).filter_by(**filter_by)
            result = await session.execute(query)
            blog_likes = result.scalar()
            return blog_likes
    
    @classmethod 
    async def get_comment_likes(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(func.count(cls.model.id)).filter_by(**filter_by)
            result = await session.execute(query)
            comment_likes = result.scalar()
            return comment_likes   
    
    @classmethod 
    async def create(cls, **values):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**values)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def delete(cls, id_):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=id_)
            await session.execute(query)
            await session.commit()
            return 'Deleted successfully'