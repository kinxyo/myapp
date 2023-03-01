from .database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, text

class products(Base):
    __tablename__ = "newproducts"
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    sale = Column(Boolean, server_default='False')
    inventory = Column(Integer, server_default='20')
    createdat = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)

