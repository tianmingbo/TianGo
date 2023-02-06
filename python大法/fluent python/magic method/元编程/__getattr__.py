# __getattr__, __getattribute__
# __getattr__ 在查找不到属性的时候调用
# __getattribute__ 属性访问优先调用


class User:
    def __init__(self, info={}):
        self.info = info

    def __getattr__(self, item):
        return self.info[item]

    def __getattribute__(self, item):
        return "test"  # 始终返回test


if __name__ == "__main__":
    user = User(info={"company_name": "ea", "name": "tian"})
    print(user.test)
