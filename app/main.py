# from urllib.request import Request
from fastapi import FastAPI, HTTPException, status, Depends, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
# from 
from pydantic import BaseModel
from typing import Optional, List
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from .votes import vote
from .posts import postroute
from .authentication import router, get_current_user

# CREATING ROUTER----------------->
app = FastAPI()
app.include_router(router, prefix="/users", tags=["UserFunctions"])
app.include_router(postroute, prefix="/posts", tags=["Posts"])
app.include_router(vote, prefix="/votes", tags=["VotesSystem"])

# TEMPLATES----------------->
templates = Jinja2Templates(directory="frontend")


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


# HELLO WORLD----------------->
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# ALLOW CORS----------------->
origins = ['http://127.0.0.1:5500'] # You can add in the list whichever domains you want to allow access to your API. If you want to allow access to all domains, you can use "*".

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#console.log("Hello World")
print("Hello World")

# FRONTEND----------------->
# @app.get("/f/{test}")
# def frontend(request: Request, test: str = "Kinxyo", response_class = HTMLResponse):
#     return templates.TemplateResponse("index.html", {"request": request, "pop": test})
@app.get("/")
def frontend(request: Request, response_class = HTMLResponse):
    return templates.TemplateResponse("index.html", {"request": request})
    

# @app.post("/submitform")
# def submitform(request: Request, title: str = Form(...), description: str = Form(...), image: UploadFile = File(...)):
#     return {"title": title, "description": description, "image": image}

# @app.post("/submitform")
# async def submitform(user: any.user = Form(...), pass: any.password = Form(...)):
#     return {"user": user, "pass": pass}

@app.post("/submitform")
async def submitform(user: str = Form(...), files: UploadFile = File(...)):
    print(files.filename)
    filecontent = await files.read()
    return {"user": user, "msg": filecontent}

# @app.post("/yo")
# async def yo(user: str = Form(), pass: str = Form()):
#     print(user, pass)
#     return {"msg1": user, "msg2": pass}

@app.post("/yo")
async def yo(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}

class any(BaseModel):
    title: str = Form(...)
    content: str = Form(...)

@app.post("/test")
async def test(title: str = Form(...), content: str = Form(...)):
    return {"title": title, "content": content}

# @app.post("/test")
# async def test(payload: any = Form(embed=True)):
# # async def test(var1: any.title = Form(...), var2: any.content = Form(...)):
#     # payload_dict = payload.dict()
#     print(payload)
#     return payload
