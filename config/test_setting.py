from . import base_setting


class TestSetting(base_setting.BaseSetting):
    DEBUG = False
    SERVER_PORT = 8080
    APP_NAME = "Capital-DC-A[test]"