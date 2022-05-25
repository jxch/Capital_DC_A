from flask import Flask
from flask_apscheduler import APScheduler
import os
import py_eureka_client.eureka_client as eureka_client
from config import config_dict
from dc import daily, init
import traceback, threading


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
app = Flask(__name__)

env = os.getenv('CAPITAL_DC_A_ENV')
app.config.from_object(config_dict[env])
# app.config.from_object(config_dict['dev'])

print("当前环境: " + env)

eureka_client.init(eureka_server=app.config.get('EUREKA_SERVER'),
                   app_name=app.config.get('APP_NAME'),
                   instance_host=app.config.get('SERVER_HOST'),
                   instance_port=app.config.get('SERVER_PORT'),
                   ha_strategy=eureka_client.HA_STRATEGY_RANDOM)


@app.route('/')
def hello_world():  # put application's code here
    return 'Capital DC A Service!'


@app.route('/init')
def app_init():
    try:
        threading.Thread(target=init, name='thread-init').start()
    except Exception:
        traceback.print_exc()
    return 'init thread start!'


@scheduler.task('cron', id='stock_daily', day='*', hour='10', minute='0', second='0')
def daily_job():
    print("daily - job", flush=True)
    daily()
    print("执行每日更新计划完毕!", flush=True)


if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=app.config.get('DEBUG'),
            threaded=app.config.get('THREADED'),
            port=app.config.get('SERVER_PORT'),
            host=app.config.get('HOST'))
