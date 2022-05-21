from config import pro, engine_qbh_capital
import pandas as pd
from dc.model.Stock import Stock
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR


def stock_daily_job():
    stock_sse = pro.stock_basic(exchange='SSE', list_status='L', fields='symbol, name')
    stock_szse = pro.stock_basic(exchange='SZSE', list_status='L', fields='symbol, name')
    stock_bse = pro.stock_basic(exchange='BSE', list_status='L', fields='symbol, name')
    stock_sse.set_index(['symbol'], inplace=True)
    stock_szse.set_index(['symbol'], inplace=True)
    stock_bse.set_index(['symbol'], inplace=True)
    stock_sse['exchange'] = 'SSE'
    stock_szse['exchange'] = 'SZSE'
    stock_bse['exchange'] = 'BSE'
    stocks = pd.concat([stock_sse, stock_szse, stock_bse])

    print("准备写入数据库", flush=True)

    engine = engine_qbh_capital()
    session = sessionmaker(bind=engine)()

    try:
        pd.io.sql.to_sql(stocks, Stock.__tablename__, engine, if_exists='replace',
                         dtype={'symbol': VARCHAR(6), 'name': VARCHAR(10), 'exchange': VARCHAR(4)})
        print("update success!", flush=True)
    except Exception:
        traceback.print_exc()
        print("update fail!", flush=True)
    finally:
        session.close()
        engine.dispose()
