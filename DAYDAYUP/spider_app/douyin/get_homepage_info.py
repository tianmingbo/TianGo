# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 9:57
# @Author  : tmb
import requests
import re


def get_homePage_info():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    res = requests.get(
        'https://www.iesdouyin.com/share/user/70820101407?sec_uid=MS4wLjABAAAAiTZzXO5F8MMmwB5tTesW8gk7xQNOhieGH13f_aVQS0U&timestamp=1602559725&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin',
        headers=headers)
    print(res.text)


if __name__ == '__main__':
    get_homePage_info()
