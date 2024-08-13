from fastapi import APIRouter
from blog import database, schemas
from typing import List
from fastapi import Depends , status
from sqlalchemy.orm import Session
from blog.repository import user

router = APIRouter(tags=['Users'],prefix="/user")


@router.post('/',response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request:schemas.User, db: Session = Depends(database.get_db)):
    return user.create_user(db, request)

@router.get('/{id}',response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id:int,db:Session = Depends(database.get_db)):
    return user.get_user(db, id)

@router.get('/',response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_all_users(db:Session = Depends(database.get_db)):
    return user.get_all_users(db)