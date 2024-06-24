import requests

"""
json web token
常用在前后端分离项目中
"""


def get_jwt():
    url = 'https://login3.scrape.center/api/login'
    data = {'username': "admin", 'password': "admin"}
    res = requests.post(url, data=data)
    print(res.json())
    return res.json()['token']


def get_book_info(jwt_info):
    headers = {'Authorization': f'jwt {jwt_info}'}
    url = 'https://login3.scrape.center/api/book/?limit=18&offset=18'
    res = requests.get(url, headers=headers)
    print(res.json())


if __name__ == '__main__':
    jwt_info = get_jwt()
    get_book_info(jwt_info)
