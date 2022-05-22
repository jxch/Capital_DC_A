from config import pro, engine_qbh_capital
import pandas as pd
from dc.model.Stock import Stock
from dc.model.StockKLines import StockKLinesDaily
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR, DATE
import time


def convert(data):
    data = data.rename(columns={'ts_code': 'symbol'})
    data = data.rename(columns={'trade_date': 'date'})
    data = data.drop(columns=['pre_close', 'pct_chg', 'change', 'amount'])
    data.set_index(['symbol', 'date'], inplace=True)
    return data


engine = engine_qbh_capital()
session = sessionmaker(bind=engine)()
print("准备查询数据库", flush=True)
try:
    all_stock = session.query(Stock).all()
    n = 1000
    for stocks in [all_stock[i:i + n] for i in range(0, len(all_stock), n)]:
        ts_codes = ''
        for stock in stocks:
            ts_codes = ts_codes + stock.ts_code() + ','
        ts_codes = ts_codes[:-1]

        data = pro.daily(ts_code=ts_codes,
                         start_date='20220520',
                         end_date=StockKLinesDaily.end_date())
        print(data)
    # pd.io.sql.to_sql(convert(data), StockKLinesDaily.__tablename__, engine, if_exists='append',
    #                  dtype={'date': DATE, 'symbol': VARCHAR(6)})
    print("[daily-job] insert stock daily kline success!", flush=True)
except Exception:
    traceback.print_exc()
    print("[daily-job] insert stock daily kline fail!", flush=True)
finally:
    session.close()
    engine.dispose()
