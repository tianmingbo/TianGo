"""
http://jzsc.mohurd.gov.cn/data/company
使用nodejs构建api，python调用api
"""
import requests

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "jzsc.mohurd.gov.cn",
    "Referer": "http://jzsc.mohurd.gov.cn/data/company",
    "timeout": "30000",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
}
url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=1&pgsz=15&total=0'
res = requests.get(url, headers=headers)
data = {
    't': res.text
}
res = requests.post('http://127.0.0.1:6666/data', data=data)
print(res.text)
