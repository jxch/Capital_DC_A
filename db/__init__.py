from sqlalchemy import create_engine
from app import app


def engine_capital():
    return create_engine(app.config.get('DB_CAPITAL'), encoding='utf8', pool_timeout=1000)
