from time import time
from typing import Optional, List, Dict, Any, Union
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from .import models
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# use (db: Session = Depends(get_db)) to get the database session everytime you wish to connect with the database. It automatically closes the connection after the function is done which is why we use the yield statement.
 
@app.get("/products")
def tp(db: Session = Depends(get_db)):
    pop = db.query(models.products).all()
    return {"data": pop}

@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    pop = db.query(models.products).filter(models.products.id == id).first()
    if not pop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} is not found")
    return pop

# rub = (models.products.dict(),)

# class products(BaseModel): 
#     name = str
#     price = float
#     id = int
#     sale = bool = False
#     inventory = Optional[int] = 20


@app.post("/products ", status_code=status.HTTP_201_CREATED)
def create_product(db: Session = Depends(get_db)):
    models.products(name=models.products.name, price=models.products.price, sale=models.products.sale, inventory=models.products.inventory)
    return {"data": "pop"}

# abandoning this shitshow orm because the retard teaching 19 hour tutorial couldn't fucking address how to pass an imported pydantic model to response body.

# @app.post("/products")
# def create_product(product: models.products, db: Session = Depends(get_db)):
#     db.add(product)
#     db.commit()
#     db.refresh(product)
#     return product
# for some reason, this doesn't work. I don't know why. I'm going to try to figure it out later.

