from . import stock_daily


def daily():
    print("daily job start",  flush=True)
    stock_daily.stock_daily_job()
    stock_daily.stock_daily_kline_job()


def init():
    print("init start",  flush=True)
    stock_daily.stock_daily_job()
    stock_daily.stock_daily_kline_init()
