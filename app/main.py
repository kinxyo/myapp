from enum import auto
from fastapi import FastAPI, HTTPException, status, Depends
from .authentication import router, get_current_user
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
app.include_router(router, prefix="/users", tags=["UserFunctions"])

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='kinxyo', cursor_factory=RealDictCursor)
        cur = conn.cursor() # Create a cursor to perform database operations
        break
    except Exception as error:
        print('Error connecting to database')
        # print(error)
        time.sleep(5) # Wait 5 seconds before trying again

class posts(BaseModel):
    title: str
    content: str

@app.get("/")
def read_root():
    return "Welcome to the website!"

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(p: posts, user: str = Depends(get_current_user)):
    print(user)
    try:
        cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (p.title, p.content))
        conn.commit()
        return "Post created successfully, Open feed to view."
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post already exists with that title")

@app.get("/posts")
def feed():
    cur.execute("SELECT * FROM posts")
    return cur.fetchall()