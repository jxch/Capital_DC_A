from . import stock_daily


def daily():
    stock_daily.stock_daily_job()
    stock_daily.stock_daily_kline_job()


def init():
    stock_daily.stock_daily_job()
    stock_daily.stock_daily_kline_init()
