from fastapi import FastAPI
import uvicorn
from db.base import async_session_maker, engine
from endpoints import user_endpoint, blog_endpoint, comments, auth, likes
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.base import Base
from db.models.user import User
from db.models.roles import Role
from db.models.blog import Blog

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    print("Shutting down...")
    await engine.dispose()
    
app = FastAPI(title="Blog", lifespan=lifespan)

app.include_router(likes.router, prefix="/like", tags=["likes"])

app.include_router(auth.router, prefix = "/auth", tags=["auth"])

app.include_router(user_endpoint.router, prefix="/user", tags=["users"])

app.include_router(blog_endpoint.router, prefix="/blog", tags=["blog"])

app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
    
