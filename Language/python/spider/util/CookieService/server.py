# 1. cookie保存在redis中应该使用什么数据结构
# 2. 数据结构应该满足： 1. 可以随机获取 2. 可以防止重复 - set
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

import redis


# 1. 如何确保每一个网站都会被单独的运行
class CookieServer():
    def __init__(self, settings):
        self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        self.service_list = []
        self.settings = settings

    def register(self, cls):
        self.service_list.append(cls)

    def login_service(self, srv):
        while 1:
            srv_cli = srv(self.settings)
            srv_name = srv_cli.name
            cookie_nums = self.redis_cli.scard(self.settings.Accounts[srv_name]["cookie_key"])
            if cookie_nums < self.settings.Accounts[srv_name]["max_cookie_nums"]:
                cookie_dict = srv_cli.login()
                self.redis_cli.sadd(self.settings.Accounts[srv_name]["cookie_key"], json.dumps(cookie_dict))
            else:
                print("{srv_name} 的cookie池已满，等待10s".format(srv_name=srv_name))
                time.sleep(10)

    # celery
    def check_cookie_service(self, srv):
        while 1:
            print("开始检测cookie是否可用")
            srv_cli = srv(self.settings)
            srv_name = srv_cli.name
            all_cookies = self.redis_cli.smembers(self.settings.Accounts[srv_name]["cookie_key"])
            print("目前可用cookie数量: {}".format(len(all_cookies)))
            for cookie_str in all_cookies:
                print("获取到cookie: {}".format(cookie_str))
                cookie_dict = json.loads(cookie_str)
                valid = srv_cli.check_cookie(cookie_dict)
                if valid:
                    print("cookie 有效")
                else:
                    print("cookie已经失效， 删除cookie")
                    self.redis_cli.srem(self.settings.Accounts[srv_name]["cookie_key"], cookie_str)
            # 设置间隔，防止出现请求过于频繁，导致本来没失效的cookie失效了
            interval = self.settings.Accounts[srv_name]["check_interval"]
            print("{}s 后重新开始检测cookie".format(interval))
            time.sleep(interval)

    def start(self):
        task_list = []
        print("启动登录服务")
        login_executor = ThreadPoolExecutor(max_workers=5)
        for srv in self.service_list:
            task = login_executor.submit(partial(self.login_service, srv))
            task_list.append(task)

        print("启动cookie检测服务")
        check_executor = ThreadPoolExecutor(max_workers=5)
        for srv in self.service_list:
            task = check_executor.submit(partial(self.check_cookie_service, srv))
            task_list.append(task)

        for future in as_completed(task_list):
            data = future.result()
            print(data)
