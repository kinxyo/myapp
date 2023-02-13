from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
router = APIRouter(tags=['Authentication'])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='kinxyo', cursor_factory=RealDictCursor)
        cur = conn.cursor() # Create a cursor to perform database operations
        break
    except Exception as error:
        print('Error connecting to database')
        print(error)
        time.sleep(5) # Wait 5 seconds before trying again

class users(BaseModel):
    email: EmailStr
    password: str

@app.get("/users")
def check():
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

@app.post("/users", status_code=status.HTTP_201_CREATED)
def cuser(u: users):
    # hashing the password
    u.password = pwd.hash(u.password)
    try:
        # print(akjhsdkj)
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (u.email, u.password))
        conn.commit()
        return {u.email: "Registered"}
    except:
        # print("exception working")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists with that email")

@app.post("/searchid")
def sid(u: users):
    cur.execute("SELECT id FROM users where email = %s", (u.email,))
    res = cur.fetchone()
    # print("value is gonna be printed:")
    # print(res)
    return f"{u.email}'s ID: {res['id']}"


@app.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
def duser(u: users):
    cur.execute("DELETE FROM users WHERE email = %s AND password = %s", (u.email, pwd.hash(u.password)))
    conn.commit()
    return u
    # u.password = 


@app.delete("/users/{id}")
def duser(id: str):
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    return {"success": True}
    # return {"success": True}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/users/{id}")
def verify(id: str):
    cur.execute("SELECT email FROM users WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # cur.execute("SELECT email FROM users WHERE id = %s", (id,))
    # lol = cur.fetchone()
    return {res['email']: "Verified"}

@router.post("/login")
def login(u: users):
    cur.execute("SELECT * FROM users WHERE email = %s", (u.email,))
    res = cur.fetchone()
    # u.password = pwd.hash(u.password)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pwd.verify(u.password, res['password']):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    return {"success": True}

@app.post("/bpm")
def bpm(u: users):
    return {u.email, u.password}