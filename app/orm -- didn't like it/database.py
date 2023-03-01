from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import time

while True:
    try:
        engine = create_engine('postgresql://postgres:kinxyo@localhost:5432/fastapi')
        sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        session = sessionlocal()
        break
    except Exception as error:
        print('Error connecting to database')
        print(error)
        time.sleep(5) # Wait 5 seconds before trying again

Base = declarative_base()
 
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
