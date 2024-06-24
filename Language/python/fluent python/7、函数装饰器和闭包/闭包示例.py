# class Averager():
#     def __init__(self):
#         self.series = []
#
#     def __call__(self, new_value):
#         self.series.append(new_value)
#         total = sum(self.series)
#         return total / len(self.series)
#
#
# avg = Averager()
# print(avg(10))


def make_average():
    series = []  # series是自由变量

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return average


def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1  # 不使用nonlocal，则count和total会创建局部变量，不能使用闭包
        total += new_value
        return total / count

    return averager


avg = make_average()
print(avg(10))
print(avg.__name__)
print(avg.__code__.co_varnames)
