from fastapi import FastAPI
from blog.routers import authentication, blog, user
from . import models,database

app = FastAPI()
models.Base.metadata.create_all(database.engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
    
