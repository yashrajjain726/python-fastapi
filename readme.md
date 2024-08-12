# FastAPI Models and Schemas

In FastAPI, the terms "model" and "schema" refer to different aspects of handling data within your application, particularly when interacting with databases and defining API endpoints.

## Models

Models in FastAPI typically refer to SQLAlchemy ORM (Object Relational Mapper) classes that represent database tables. These models define the structure of your database tables and establish relationships between them. They are used to perform CRUD operations on the database directly. Here's an example of models representing `User` and `Item` tables:

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")
```

## Schemas

Schemas, on the other hand, are Pydantic models used to define the structure of request bodies, query parameters, and response models for API endpoints. They serve as a contract for the data exchanged between the client and the server. Schemas can also include validation rules and metadata for API documentation. Here's an example of schemas for creating and retrieving items:

```python
from typing import List, Union
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
```

## Use Cases and Examples

- **Models** are used when interacting directly with the database. For example, when creating a new item associated with a user, you would use the `Item` model to insert a new record into the database.

- **Schemas** are used to validate and serialize/deserialize data in API endpoints. For instance, when defining an endpoint to create a new item, you would use the `ItemCreate` schema to validate the request body and possibly return a serialized representation of the newly created item using the `Item` schema.

Here's an example of an endpoint that uses both a model and a schema:

```python
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

In this example, the `create_item` endpoint accepts data validated by the `ItemCreate` schema, converts it into a model instance (`models.Item`), and saves it to the database. The response is then serialized using the `Item` schema, which includes ORM mode to handle SQLAlchemy objects properly.

## Summary

- **Models** are used for database interactions and represent the structure of your database tables.
- **Schemas** define the structure of request and response bodies for API endpoints, including validation rules and metadata for documentation.
- Both models and schemas play crucial roles in FastAPI applications, serving different purposes in handling data and interactions with databases and clients.
