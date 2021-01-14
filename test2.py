a = (1, '永兴东路与魏文路交叉口', 'crossroad-3-20', '4', '河南省-许昌市-示范区', 1, '113.863312', '34.092056', '192.168.10.14', 2, 1, 1, 1,
     '{"plan_num": 3, "conductor": "system", "from": {"control_type": 1, "plan_num": 3}, "source": 1, "emergency_status": 2, "period_id": 2}')
b = ('id', 'name', 'number', 'region', 'address', 'type', 'longitude',
     'latitude', 'telese_ip', 'car_collect_type', 'person_collect_type', 'is_setted',
     'control_type', 'control_detail')
dic = {i: a[b.index(i)] for i in b}
print(dic)
