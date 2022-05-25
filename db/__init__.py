from sqlalchemy import create_engine
from flask import Flask, current_app

app = Flask(__name__)


def engine_capital():
    with app.app_context():
        return create_engine(current_app.config.get('DB_CAPITAL'), encoding='utf8', pool_timeout=1000)
