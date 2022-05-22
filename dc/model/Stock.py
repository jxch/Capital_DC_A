from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    symbol = Column(String(6), primary_key=True)
    name = Column(String(10))
    exchange = Column(String(4))

    def ts_code(self):
        if self.exchange == 'SZSE':
            return self.symbol + '.' + 'SZ'
        elif self.exchange == 'SSE':
            return self.symbol + '.' + 'SH'
        elif self.exchange == 'BSE':
            return self.symbol + '.' + 'BJ'
        else:
            raise Exception("错误的股票代码!", self.symbol, self.exchange, self.name)
