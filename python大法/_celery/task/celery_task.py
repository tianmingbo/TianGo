# task01
import time
from .celery import app


@app.task
def send_email(res):
    time.sleep(5)
    return "完成向%s发送邮件任务" % res


@app.task
def send_msg(name):
    time.sleep(5)
    return "完成向%s发送短信任务" % name
