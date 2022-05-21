import tushare as ts
from sqlalchemy import create_engine

from . import dev_setting
from . import product_setting
from . import test_setting
from . import local_setting


def engine_qbh_capital():
    return create_engine('mysql+pymysql://root:jiang155.@jiangxicheng.xyz:3306/capital', encoding='utf8',
                         pool_timeout=1000)


pro = ts.pro_api('34af7b2e7f3bbf2c48b0a12e0084c9099df78acd66f37ad5c92e0326')

config_dict = {
    'default': local_setting.LocalSetting,
    'dev': dev_setting.DevSetting,
    'test': test_setting.TestSetting,
    'local': local_setting.LocalSetting,
    'product': product_setting.ProductSetting
}
