from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='kinxyo', cursor_factory=RealDictCursor)
        cur = conn.cursor() # Create a cursor to perform database operations
        break
    except Exception as error:
        print('Error connecting to database')
        print(error)
        time.sleep(5) # Wait 5 seconds before trying again

@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM products")
    return cur.fetchall()

class products(BaseModel):
    name: str
    price: float
    inventory: int

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: products):
    cur.execute("INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s)", (post.name, post.price, post.inventory))
     
    conn.commit()
    return post

@app.get("/posts/{id}")
def get_post(id: str):
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return res

#probably known as 'trailing comma', like at line 40, we added addition comma after id. I have no idea what it does but without it, I run into weird error like I should be getting 404 error for entering invalid id but instead I get 500 error. I don't know why but it works with it.
#issue-solved: From the Psycopg docs: "For positional variables binding, the second argument must always be a sequence, even if it contains a single variable (remember that Python requires a comma to create a single element tuple):" The error is there because it expects an object that supports indexing, so putting a comma after id would make it indexable. To add some more context, the indexing issue is because he is trying to pass a tuple with a single value. Tuples with a single value requires a comma after the value. With out the comma, python doesn't recognize it as a tuple, and that's creating the error.


@app.put("/posts/{id}")
def update_post(id: str, post: products):
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    cur.execute("UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s", (post.name, post.price, post.inventory, id))
    conn.commit()
    return post

@app.delete("/posts/{id}")
def delete_post(id: str):
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    res = cur.fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    return {"success": True}
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

'''
This is one way to connect with database (by directly using rawsql)
but there is another way to connect with database using ORM (Object Relational Mapping). Let's just learn it incase it comes handy. The basic idea is that you write everything in python and it will be converted to sql. It's like writing sql in python. It's called SQLAlchemy. It's a python library that allows you to write sql in python.
pip install sqlalchemy
pip install psycopg2 (because sqlalchemy doesn't know how to talk to database, it needs a driver to talk to database. psycopg2 is a driver for postgresql)
Lastly, the main benefit of using ORM is that you can create a separate file for your database models without cluttering your main file.
(Lastly, we can use asyncpg instead of psycopg2. It's faster than   psycopg2. It's a driver for postgresql. --COPILOT SUGGESTED THIS--)
''' 