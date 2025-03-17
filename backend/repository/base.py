from abc import ABC, abstractmethod
from typing import List, Union
from db.base import async_session_maker
from sqlalchemy import select, update, delete, insert

class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod 
    async def get_all(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def get_one_or_none(**filter_by):
        pass 
    
    @staticmethod
    @abstractmethod 
    async def get_by_id(id_):
        pass
    
    @staticmethod
    @abstractmethod
    async def get_by_email(email):
        pass
    
    @staticmethod
    @abstractmethod 
    async def create(**values):
        pass   
    
    @staticmethod
    @abstractmethod 
    async def update(id_, **values):
        pass
    
    @staticmethod
    @abstractmethod 
    async def delete(id_):
        pass 

class BaseRepository(AbstractRepository):
    model = None
    model_pydantic_schema = None
    
    @classmethod
    async def get_all(cls, limit, skip, **filter_by) -> model_pydantic_schema:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [cls.model_pydantic_schema(**elem) for elem in mapping_result]
                                            
    @classmethod
    async def get_one_or_none(cls, **filter_by) -> model_pydantic_schema:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by) 
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return cls.model_pydantic_schema(**mapping_result) if mapping_result else None    
                            
    @classmethod    
    async def get_by_id(cls, id_) -> model_pydantic_schema:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=id_)
            result = await session.execute(query)
            mapping_result = result.mappings().first()
        return cls.model_pydantic_schema(**mapping_result) if mapping_result else None
    
    @classmethod
    async def get_by_email(cls, email_) -> model_pydantic_schema:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(email=email_)
            result = await session.execute(query)
            mapping_result = result.mappings().first()
            return cls.model_pydantic_schema(**mapping_result) if mapping_result else None
        
    
    @classmethod
    async def create(cls, **values) -> None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**values)
            result = await session.execute(query)
            await session.commit()
            
    @classmethod
    async def update(cls, id_, **values) -> id:
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(id=id_).values(**values).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit() 
            return result.scalar()  
        
    @classmethod
    async def delete(cls, id_) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=id_)
            await session.execute(query)
            await session.commit()
            return "Deleted successfully"
            

    
    