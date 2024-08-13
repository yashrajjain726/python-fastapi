from fastapi import APIRouter

from blog import database, models, schemas
from blog.repository import blog
from ..schemas import Blog
from typing import List
from fastapi import Depends , status, Response, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["Blogs"],prefix="/blog")

@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
def get_all_blogs(db:Session = Depends(database.get_db)):
    return blog.get_all_blogs(db)

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def get_blog_by_id(id,db:Session = Depends(database.get_db)):
    return blog.get_blog_by_id(id,db)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ShowBlog)
def create_blog(request: schemas.Blog, db:Session = Depends(database.get_db)):
    return blog.create_blog(request,db)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):        
    return blog.delete_blog(id,db)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request: schemas.Blog,db: Session = Depends(database.get_db)):
    return blog.update_blog(id,request,db)

