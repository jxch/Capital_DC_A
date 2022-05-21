from flask import Flask
from flask_apscheduler import APScheduler
from dc import daily_job


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Capital DC A Service!'


@app.route('/init')
def init():
    daily_job()
    return 'init success!'


@scheduler.task('cron', id='stock_daily', day='*', hour='1', minute='1', second='1')
def daily_job():
    daily_job()
    print("执行每日更新计划完毕!")


if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run()
