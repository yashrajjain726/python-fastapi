from typing import List
from fastapi import FastAPI, Depends , status, Response, HTTPException

from blog.hashing import Hash
from . import models,database,schemas
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
def get_all_blogs(response: Response,db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return {"message": "No blogs found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blogs found")
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def get_blog_by_id(id,response: Response,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return {"message": "Blog not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):        
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request: schemas.Blog,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return {"message": "Blog updated successfully", "data": updated_blog}




#  USER
@app.post('/user',response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "data": new_user}

@app.get('/user/{id}',response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).where(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user

@app.get('/users',response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No users found")
    return users
    
