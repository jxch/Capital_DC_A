import tushare as ts
from sqlalchemy import create_engine


def engine_qbh_capital():
    return create_engine('mysql+pymysql://root:jiang155.@jiangxicheng.xyz:3306/capital', encoding='utf8')


pro = ts.pro_api('34af7b2e7f3bbf2c48b0a12e0084c9099df78acd66f37ad5c92e0326')
