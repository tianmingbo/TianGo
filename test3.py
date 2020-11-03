import json
from datetime import datetime

period_details = {(0, 0): [1, 3]}
# time = (datetime.now().hour, datetime.now().minute)
# index = 0
# for i in period_details:
#     if list(i.keys())[0][0] <= time[0]:
#         index += 1
# tmp = index - 1
# for i in period_details[tmp:]:
#     # print(list(i.keys())[0][1])
#     if list(i.keys())[0][1] > time[1]:
#         index -= 1
#         break
# print(index)
# print(period_details[3])
a = {'begin_time': '30:60', 'control_type': 1, 'timing_plan_id': 2}
print(a['begin_time'][3])
if int(a['begin_time'][3]) * 10 + int(a['begin_time'][4]) >= 60:
    print('err')
