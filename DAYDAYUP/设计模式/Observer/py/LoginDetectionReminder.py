import time

from template import Observer, Observable


class Account(Observable):
    """账户作为被观察者"""

    def __init__(self):
        super().__init__()
        self.__last_ip = {}
        self.__last_region = {}

    def login(self, name, ip, _time):
        region = self.__get_region(ip)
        if self.__is_login_distance(name, region):
            self.notify_observer({'name': name, 'ip': ip, 'region': region, 'time': _time})
        self.__last_region[name] = region
        self.__last_ip[name] = ip

    @staticmethod
    def __get_region(ip):
        """根据ip获取地区"""
        ip_regions = {
            '1.1.1.1': "hn",
            '2.2.2.2': 'sh'
        }
        return ip_regions[ip]

    def __is_login_distance(self, name, region):
        latest_region = self.__last_region.get(name)
        return latest_region is not None and latest_region != region


class SmsSender(Observer):
    """作为登录监听者"""

    def update(self, observable, obj):
        print(obj)


if __name__ == '__main__':
    account = Account()
    account.add_observer(SmsSender())
    account.login("dali", "1.1.1.1", time.time())
    account.login("dali", "2.2.2.2", time.time())
