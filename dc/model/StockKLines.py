from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATE, FLOAT
import datetime

Base = declarative_base()


class StockKLinesDaily(Base):
    __tablename__ = 'stock_kline_daily'
    symbol = Column(String(6), primary_key=True)
    date = Column(DATE, primary_key=True)
    open = Column(FLOAT)
    high = Column(FLOAT)
    low = Column(FLOAT)
    close = Column(FLOAT)
    vol = Column(FLOAT)

    @classmethod
    def start_date(cls):
        return '20200101'

    @classmethod
    def end_date(cls):
        return datetime.date.today().strftime('%Y%m%d')
