import tushare as ts
from sqlalchemy import create_engine
from flask import current_app

from . import dev_setting
from . import product_setting
from . import product_china_setting
from . import test_setting
from . import local_setting


def engine_capital():
    print("当前数据源: " + current_app.config.get('DB_CAPITAL'))
    return create_engine(current_app.config.get('DB_CAPITAL'), encoding='utf8', pool_timeout=1000)


pro = ts.pro_api('34af7b2e7f3bbf2c48b0a12e0084c9099df78acd66f37ad5c92e0326')

config_dict = {
    'default': local_setting.LocalSetting,
    'dev': dev_setting.DevSetting,
    'test': test_setting.TestSetting,
    'local': local_setting.LocalSetting,
    'product': product_setting.ProductSetting,
    'product_china': product_china_setting.ProductChinaSetting
}
