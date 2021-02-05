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
    series = []

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return average


avg = make_average()
print(avg(10))
print(avg.__name__)
print(avg.__code__.co_varnames)
