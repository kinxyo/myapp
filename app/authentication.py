#IMPORTING LIBRARIES----------------->
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.params import Body
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
from jose import JWTError, jwt
import time
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


# CREATING ROUTER----------------->
router = APIRouter()
templates = Jinja2Templates(directory="frontend")

# CONNECTING TO DATABASE----------------->
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='kinxyo', cursor_factory=RealDictCursor)
        cur = conn.cursor() # Create a cursor to perform database operations
        break
    except Exception as error:
        print('Error connecting to database')
        print(error)
        time.sleep(5) # Wait 5 seconds before trying again

# SCHEMA MODEL----------------->
class users(BaseModel):
    email: EmailStr
    password: str

class tokendata(BaseModel):
    email: Optional[EmailStr] = None

# USER FUNCTIONS----------------->
@router.post("/", status_code=status.HTTP_201_CREATED)
# def cuser(u: users):
def cuser(email: str = Form(), password: str = Form()):
    try:
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, pwd.hash(password)))
        conn.commit()
        return {email: "Registered"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists with that email")

@router.get("/")
def check():
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

@router.get("/{id}")
def verify(id: str):
    cur.execute("SELECT email FROM users WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {res['email']: "Verified"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def duser(u: users):
    cur.execute("DELETE FROM users WHERE email = %s AND password = %s", (u.email, pwd.hash(u.password)))
    conn.commit()
    return u

@router.delete("/{id}")
def duser(id: str):
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    res = cur.fetchone()
    print(res)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    return {"success": True}

@router.put("/{id}")
def uuser(id: str, u: users):
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    cur.execute("UPDATE users SET email = %s, password = %s WHERE id = %s", (u.email, pwd.hash(u.password), id))
    conn.commit()
    return {"success": True}

#AUTHENTICATION----------------->
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

#authentication setup (also need to be shifted to env file)
key = "secret" 
algorithm = "HS256"
tokenexp = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=tokenexp)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt

@router.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
# async def login(request: Request, u: OAuth2PasswordRequestForm = Depends(), username: str = Form(), password: str = Form()):
# def login(u: OAuth2PasswordRequestForm = Depends()):
    # # u.username = username
    # u.password = password
    # print(u.username)
    # print(u.password)
    # return "cool"
    # cur.execute("SELECT * FROM users WHERE email = %s", (u.username,))
    cur.execute("SELECT * FROM users WHERE email = %s", (username,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # if not pwd.verify(u.password, res['password']):
    if not pwd.verify(password, res['password']):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect password")
    access_token = create_access_token(data={"sub": username})
    # print(access_token)
    return access_token
    # return {access_token: templates.TemplateResponse("index.html", {"request": request})}
    # return templates.TemplateResponse("index.html", {"request": request})

def verify_access_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login"))):
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        token_data = tokendata(email=email)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, header={"WWW-Authenticate": "Bearer"})
    return token_data

@router.get("/me")
def get_current_user(token_data: users = Depends(verify_access_token)):
    return token_data
    # print(token_data)



# MISCELLENOUS FUNCTIONS----------------->
@router.post("/searchid")
def sid(u: users):
    cur.execute("SELECT id FROM users where email = %s", (u.email,))
    res = cur.fetchone()
    return f"{u.email}'s ID: {res['id']}"

@router.post("/bpm")
def bpm(u: users):
   email: str = "test@gmail.com"
   if email == u.email:
       return u.email 
   return "Not found"