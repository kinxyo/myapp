from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

#this file covers all the basic operations of fastapi (CRUD)

app = FastAPI()

class class1(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


@app.get("/")
def temp():
    return {"message": "hello w"}

# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts}

# @app.post("/posts")
# def func1(var1: class1): #taking reference of a class as a avariable
#     print(var1)
#     return {"data":"new post"}

# @app.post("/posts")
# def func1(var1: class1): #taking reference of a class as a avariable
#     print(var1.publish)
#     print(var1.rating)
#     return {"data":"new post"}

'''
@app.post("/posts")
def func1(var1: class1): #taking reference of a class as a avariable
    print(var1.dict()) #what .dict() does here is basically all our inputs are stored as pydantic model so it just coverts them into dictionary/json.
    return {"data":"new post"}
'''
'''
#updating
@app.post("/posts")
def update(up: class1):
    up = up.dict()
    up['id'] = randrange(0,10000000)
    my_posts.append(up)
    return {"data": up}
'''
'''
#retrive single post
@app.get("/posts/{id}") #this is id is called path_parameter
def get_post(id): #function parameter was the id from class1
    print(id)
    return {"post_detail": f"here is post {id}"}
'''
my_posts = [
    {"Show": "Attack on Titans","FavChar": "Levi Ackerman","id": 1},
    {"Show": "Jujutsu Kaisen 0","FavChar":"Yuta Okotsu","id": 2},
    {"Show": "Jojo's Bizzare Adventure Part 7: Steel Ball Run","FavChar":"Gyro Zeppeli","id": 4},
    {"Show": "Naruto","FavChar":"Itachi Uchiha","id": 3}
    ]

def findpost(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# ERROR 404 ONE WAY TO SHOW        
# @app.get("/post/{id}")
# def get_post(id, response: Response):
#     post = findpost(int(id))
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"ERROR": "Post Not Found At Requested Id"}
#     return {"data": post}

@app.get("/post/{id}")
def get_post(id: int):
    post = findpost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found At Requested Id")
    return {"data": post}

@app.get("/post")
def get_all():
    return {"data": my_posts}

class show(BaseModel):
    Show:  str
    FavChar: str
    id: Optional[int] = None

@app.post("/post")
def create_post(post: show): #show is currently a pydantic model
    newman = post.dict() #converting pydantic model to dictionary
    newman['id'] = randrange(4,10) #normally database does this but we are doing it manually so we are generating a random number.
    my_posts.append(newman)
    # my_posts.append(post.dict()) is also possible
    return {"data": newman}

@app.delete("/post/{id}")
def delete_post(id: int):
    post = findpost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found At Requested Id")
    my_posts.remove(post)
    return {"data": post}

def findindex(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

class update(BaseModel):
    Show: str
    FavChar: str

@app.put("/post/{id}")
def update_post(id: int, post: update):
    index = findindex(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found At Requested Id")
    
    upost = post.dict()
    upost['id'] = id
    my_posts[index] = upost
    return {"data": upost}

