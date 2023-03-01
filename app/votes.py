from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from .authentication import router, get_current_user
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
from .posts import postroute

# CREATING ROUTER----------------->
vote = APIRouter()

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
class votes(BaseModel):
    id: str
    upvote: int # 1 for upvote, 0 for null (removing like)
    downvote: int # 1 for downvote, 0 for null (removing dislike)

# VOTE FUNCTIONS----------------->
@vote.post("/upvote")
def upvote(id: str, user: str = Depends(get_current_user)):
    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    cur.execute("SELECT * FROM votes WHERE postid = %s AND emaillnk = %s", (id, user.email,))
    res = cur.fetchone()
    if res:
        if res['upvote'] == 1:
            cur.execute("UPDATE votes SET upvote = 0, downvote = 0 WHERE postid = %s AND emaillnk = %s", (id, user.email,))
            conn.commit()
            return "Upvote removed"
        else:
            cur.execute("UPDATE votes SET upvote = 1, downvote = 0 WHERE postid = %s AND emaillnk = %s", (id, user.email,))
            conn.commit()
            return "Upvote added"
    else:
        cur.execute("INSERT INTO votes (postid, upvote, downvote, emaillnk) VALUES (%s, %s, %s, %s)", (id, 1, 0, user.email,))
        conn.commit()
        return "Upvote added"