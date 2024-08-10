from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
data = [1,2,3,4,5,6,7,8,9,10]
@app.get("/") # get -> operation | / -> path | @app -> path operation decorator
def index(): # It is called path operation function
        return {"data": {"name": "Yashraj"}}


@app.get("/blog/unpublished")
def index():
    return {"data": "all unpublished blogs"}

@app.get("/blog")
def index(published: bool = False, limit: int = 5,sort:Optional[str] = None):
    if published:
        return {"data": data[0:limit]}
    else:
         return {"data": "all unpublished blogs"}
       


@app.get("/blog/{id}")
def index(id:int):
    return {"data":  id,}

@app.get("/blog/{id}/comments")
def index(id,limit:Optional[int]=None):
    if limit:
        return {"data": limit}  
    return {"data":'comments'}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None

@app.post("/blog")
def create_blog(blog:Blog):
    return {"data": f"Blog is created as {blog.title}"}


#  TO RUN THIS FILE IN LOCALHOST IN A NEW PORT (python main.py)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)