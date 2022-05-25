from flask import current_app
from sqlalchemy import create_engine


def engine_capital():
    return create_engine(current_app.config.get('DB_CAPITAL'), encoding='utf8', pool_timeout=1000)