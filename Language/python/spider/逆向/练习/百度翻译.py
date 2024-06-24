import json
import execjs

import requests

node = execjs.get()
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "135",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "BIDUPSID=947BB8A73DB62DA3E861F38BB27CDD3C; PSTM=1624197545; BAIDUID=947BB8A73DB62DA322823F2A550CDB4C:FG=1; __yjs_duid=1_85f8f60808391bd64d980939093d610f1624371077232; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDSFRCVID=DLAOJexroG3VPYnHRn4K2MJhN2KKv3JTDYLE8yu9T4VNR5DVgVCoEG0Pt_ZYMak-XolpogKK0eOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJKO_CP-tCt3fP36qRbqhRteKlbb5R3KHD7XVhjR3p7keq8CDl6jXxFdM47NLtRDtejZBpr1yD0-hIQ2y5jHhU-Oe-bN0PQtKC5yhUQx2h7psIJMKPDWbT8ULf50a4byaKviaKJHBMb1jpODBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6JXDa-Jtjtjf5nH3ROHHDKajR7Pq4bohjnQWfR9BtQmJJrzbM5htl71VlOCh65Yy4kND4RiQlcZQg-q3R775f7YfDometrC5444XtnR0x-jLnbOVn0MW-5DMxL654nJyUnQbtnnBPnm3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CF-fC-KhK_6jjRb5nbH2x70bPcXHD7yWCvuyfJcOR5Jj65A0nFV3M57QfJqQnruaJnktqvvVfT_3MA--t4P0nPJB4vUW2QDsRr_tKoVsq0x0hbWe-bQypoaXtRkBIOMahkM5l7xObvJQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3tjjT0DN0etTFqfKresJoq2RbhKROvhj4BQxPgyxoObtRxtacThC3dLJrAsDoEy47FDxPU5GbZLU3kBTn9LMnx--t58h3_XhjJ3xteQttjQn3dyH5u3RkEyn7Sqb7TyU42bf47yaji0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLtoKtbJII-bncGhJ3S5tC_qG_OetJyaR3R2pjvWJ5WqR7jDpjmWtCn0xIJB5juWDbwoqvcbDOkShbXXM_W2JQ-3aOpWqDt3NcM-qOO3l02V-b3WlrY-tnDWMnQbPRMW20j0l7mWIQvsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDH0Dq6bP; H_PS_PSSID=35105_31254_35237_35436_34584_35491_35246_34578_35329_35320_26350_35478; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=947BB8A73DB62DA322823F2A550CDB4C:FG=1; BDSFRCVID_BFESS=DLAOJexroG3VPYnHRn4K2MJhN2KKv3JTDYLE8yu9T4VNR5DVgVCoEG0Pt_ZYMak-XolpogKK0eOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJKO_CP-tCt3fP36qRbqhRteKlbb5R3KHD7XVhjR3p7keq8CDl6jXxFdM47NLtRDtejZBpr1yD0-hIQ2y5jHhU-Oe-bN0PQtKC5yhUQx2h7psIJMKPDWbT8ULf50a4byaKviaKJHBMb1jpODBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTD-Dhe6JXDa-Jtjtjf5nH3ROHHDKajR7Pq4bohjnQWfR9BtQmJJrzbM5htl71VlOCh65Yy4kND4RiQlcZQg-q3R775f7YfDometrC5444XtnR0x-jLnbOVn0MW-5DMxL654nJyUnQbtnnBPnm3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CF-fC-KhK_6jjRb5nbH2x70bPcXHD7yWCvuyfJcOR5Jj65A0nFV3M57QfJqQnruaJnktqvvVfT_3MA--t4P0nPJB4vUW2QDsRr_tKoVsq0x0hbWe-bQypoaXtRkBIOMahkM5l7xObvJQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3tjjT0DN0etTFqfKresJoq2RbhKROvhj4BQxPgyxoObtRxtacThC3dLJrAsDoEy47FDxPU5GbZLU3kBTn9LMnx--t58h3_XhjJ3xteQttjQn3dyH5u3RkEyn7Sqb7TyU42bf47yaji0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLtoKtbJII-bncGhJ3S5tC_qG_OetJyaR3R2pjvWJ5WqR7jDpjmWtCn0xIJB5juWDbwoqvcbDOkShbXXM_W2JQ-3aOpWqDt3NcM-qOO3l02V-b3WlrY-tnDWMnQbPRMW20j0l7mWIQvsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJEjj6jK4JKDH0Dq6bP; delPer=0; PSINO=5; BA_HECTOR=al84a4208g20a48hd01grmh680q; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1639315512,1639662797; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1639662797; __yjs_st=2_ZWFiYjEzMDA0NDU0NTdmYTRmYWI4N2QxYzkxNTZhOTVlYzIwMGZhZDliYzhkOTMzNWM2MTMzZjk3YmIzNGMzYmRjNGExYTEyNDNlMGRiY2I2N2ExNjEzNjIyYmI2YmNlNWE3MzVlNWE4ZWQ2M2FkMmU2YmFlYTAyYmE4ODU5ZDNlMjg4ZmJhNWE5NmRhZWZhNDI3ZjRhMmE2YzQyNmY0NzAxMmRkNTg2NjA2N2YxNGFiYWY2NzdhMzFlYTU3MjQzNjc2MTVjZjQzYmUyZDZiMTUyOWUzY2M0MTVmODhkYWJmZTI5MDc2ZDljMjBhYzAxOTc5YzE2ZjdmNDExMDQxMF83XzlkZjAwZGQ3; ab_sr=1.0.1_MTEzNGYxYTRjYjk3ZGQyNmI1YTAwODgyOWNiMzQzNzI1YTVlYzhjOGMyMzI2NGMwM2FhMmI5NTllNzhkYTgwMWExMGI0MWFkZmM5N2FkYWQ0MTY0NjAwYjM0NmI0MzZjMDdiNzgxZjZjMDBjZWFlMjA2MTgxNTg4Zjg2ZmFmOWFjNjdlN2UxY2I2Njg3NjY1YmM1ZWI4MTVmNTk4MWEwNQ==",
    "Host": "fanyi.baidu.com",
    "Origin": "https://fanyi.baidu.com",
    "Referer": "https://fanyi.baidu.com/?aldtype=16047",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
with open('百度翻译.js', 'r', encoding='utf-8') as f:
    ctx = node.compile(f.read())
word = input('查询单词->')
sign = ctx.eval(f'getSign("{word}")')
print(sign)
data = f'from=en&to=zh&query=cat&transtype=realtime&simple_means_flag=3&sign={sign}&token=c14671407f0de06fccb9129e87c86a2e&domain=common'
res = requests.post(url, data=data, headers=headers)
print(json.loads(res.text))
