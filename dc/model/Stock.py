from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    symbol = Column(String(6), primary_key=True)
    name = Column(String(10))
    exchange = Column(String(4))
