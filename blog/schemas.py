from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True


class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs: List[Blog] = []
    class Config:
        orm_mode = True
class ShowBlog(BaseModel):
    title: str
    body: str
    owner: Optional[ShowUser]
    class Config:
        orm_mode = True
