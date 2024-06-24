import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
cookies = {'log_Id_click': '1', ' uuid_tt_dd': '10_17094803150-1679493648816-992123',
           ' dc_session_id': '10_1679493648816.515440', ' dc_sid': '31ff6ebe56b4a9b56ab5327d1c3710ba',
           ' acw_sc__v2': '641b0a1c11056087a647d31008722e4e08187e51', ' UserName': 'T_I_A_N_', ' UserNick': '__tian__',
           ' AU': '951', ' UN': 'T_I_A_N_', ' BT': '1679493661046', ' p_uid': 'U010000',
           ' csrfToken': '847RiI7jR25En1IxsvXScpg8', ' c_first_ref': 'default',
           ' c_first_page': 'https%3A//www.csdn.net/', ' c_dsid': '11_1679493663855.971799', ' c_segment': '11',
           ' c_page_id': 'default', ' log_Id_pv': '1', ' Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac': '1679493665',
           ' Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac': '1679493665',
           ' Hm_up_6bcd52f51e9b3dce32bec4a3997715ac': '%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22T_I_A_N_%22%2C%22scope%22%3A1%7D%7D',
           ' www_red_day_last': 'red', ' log_Id_view': '3',
           ' ssxmod_itna': 'iqGOBKYvxjhDOYDXKG7maI8mDu07SDfxWbeqGXfTDZDiqAPGhDCb4zDDvEA5r+C5iZLqIxPipGDhhobGSDwxAlh8RoD',
           ' ssxmod_itna2': 'iqGOBKYvxjhDOYDXKG7maI8mDu07SDfxWbeA6uXq4+3D/z7D0x7phUUScFBvOKcfliYAOXYWdgh7cDnRwto5t79oDwrBPGcDYKxxD',
           ' dc_tos': 'rrxdw2'}

res = requests.get('https://blog.csdn.net/weixin_43582101/article/details/126729436', headers=headers, cookies=cookies)
with open('tmp.html', 'wb') as f:
    f.write(res.content)
# print(res.text)
