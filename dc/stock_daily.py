from config import pro, engine_qbh_capital
import pandas as pd
from dc.model.Stock import Stock
from dc.model.StockKLines import StockKLinesDaily
import traceback
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR, DATE
import time
from . import sql_utils


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


def stock_daily_kline_init():
    engine = engine_qbh_capital()
    session = sessionmaker(bind=engine)()
    print("准备查询数据库", flush=True)
    try:
        sql_utils.drop_if_exists(engine, StockKLinesDaily.__tablename__)
        all_stock = session.query(Stock).all()
        n = 5
        for stocks in [all_stock[i:i + n] for i in range(0, len(all_stock), n)]:
            ts_codes = ''
            for stock in stocks:
                ts_codes = ts_codes + stock.ts_code() + ','
            ts_codes = ts_codes[:-1]
            for i in range(10):
                try:
                    data = pro.daily(ts_code=ts_codes,
                                     start_date=StockKLinesDaily.start_date(),
                                     end_date=StockKLinesDaily.end_date())
                except:
                    time.sleep(60 * i)
                    print("[init-job] 1分钟后重试[" + str(i) + "/10]", flush=True)
                else:
                    pd.io.sql.to_sql(convert(data), StockKLinesDaily.__tablename__, engine, if_exists='append',
                                     dtype={'date': DATE, 'symbol': VARCHAR(6)})
        print("[init-job] insert stock daily kline success!", flush=True)
    except Exception:
        traceback.print_exc()
        print("[init-job] insert stock daily kline fail!", flush=True)
    finally:
        session.close()
        engine.dispose()


def stock_daily_kline_job():
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
            for i in range(10):
                try:
                    data = pro.daily(ts_code=ts_codes,
                                     start_date=StockKLinesDaily.end_date(),
                                     end_date=StockKLinesDaily.end_date())
                except:
                    time.sleep(60 * i)
                    print("[init-job] 1分钟后重试[" + str(i) + "/10]", flush=True)
                else:
                    pd.io.sql.to_sql(convert(data), StockKLinesDaily.__tablename__, engine, if_exists='append',
                                     dtype={'date': DATE, 'symbol': VARCHAR(6)})
        print("[daily-job] insert stock daily kline success!", flush=True)
    except Exception:
        traceback.print_exc()
        print("[daily-job] insert stock daily kline fail!", flush=True)
    finally:
        session.close()
        engine.dispose()


def convert(data):
    data['symbol'] = data['ts_code'].map(lambda ts_code: ts_code.split(".")[0])
    data = data.rename(columns={'trade_date': 'date'})
    data = data.drop(columns=['ts_code', 'pre_close', 'pct_chg', 'change', 'amount'])
    data.set_index(['symbol', 'date'], inplace=True)
    return data
