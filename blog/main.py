from typing import List
from fastapi import FastAPI, Depends , status, Response, HTTPException
from blog.hashing import Hash
from blog.routers import blog, user
from . import models,database

app = FastAPI()
models.Base.metadata.create_all(database.engine)
app.include_router(blog.router)
app.include_router(user.router)
    
