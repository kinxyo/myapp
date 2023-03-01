# IMPORTING LIBRARIES----------------->
from enum import auto
from fastapi import FastAPI, HTTPException, status, Depends, APIRouter, Form, Request
from .authentication import router, get_current_user
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# CREATING ROUTER----------------->
postroute = APIRouter()

# CONNECTING TO DATABASE----------------->
while True:
    try:
        conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_user, password=settings.database_password, cursor_factory=RealDictCursor)
        cur = conn.cursor() # Create a cursor to perform database operations
        break
    except Exception as error:
        print('Error connecting to database')
        # print(error)
        time.sleep(5) # Wait 5 seconds before trying again

# SCHEMA MODEL----------------->
class posts(BaseModel):
    title: str
    content: str

# POST FUNCTIONS----------------->
@postroute.get("/")
def feed(search: Optional[str] = None):
    if search:
        cur.execute("SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s", (f"%{search}%", f"%{search}%  ",))
        return cur.fetchall()
    else:
        cur.execute("SELECT * FROM posts")
        return cur.fetchall()

@postroute.post("/", status_code=status.HTTP_201_CREATED)
def create_post(title: str = Form(), content: str = Form(), user: str = Depends(get_current_user)):
    try:
        cur.execute("INSERT INTO posts (title, content, emaillnk) VALUES (%s, %s,%s)", (title, content,user.email))
        conn.commit()
        return "Post created successfully, Open feed to view."
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}")


@postroute.delete("/{id}")
def delete_post(id: str, user: str = Depends(get_current_user)):
    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    cur.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    return "Post deleted successfully"

@postroute.get("/my")
def my_posts(user: str = Depends(get_current_user)):
    cur.execute("SELECT * FROM posts WHERE emaillnk = %s", (user.email,))
    return cur.fetchall()

@postroute.put("/my")
def update_post(p: posts, user: str = Depends(get_current_user)):
    cur.execute("UPDATE posts SET title = %s, content = %s WHERE emaillnk = %s", (p.title, p.content, user.email))
    conn.commit()
    return "Post updated successfully"

@postroute.delete("/my")
def delete_post(user: str = Depends(get_current_user)):
    cur.execute("DELETE FROM posts WHERE emaillnk = %s", (user.email,))
    conn.commit()
    return "All posts deleted successfully"