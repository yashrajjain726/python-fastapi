from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from blog import database, models, schemas



def get_all_blogs(db:Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return {"message": "No blogs found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No blogs found")
    return blogs

def get_blog_by_id(id:int,db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).get(id)
    if not blog:
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return {"message": "Blog not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    return blog

def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

def update_blog(id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"message": "Blog updated successfully"}