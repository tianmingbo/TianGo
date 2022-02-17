# -*- coding: utf-8 -*-
# @Time    : 2020/10/21 13:24
# @Author  : tmb
import time

import requests
import pymysql

from python大法.spider.spider_app.douyin.save_db import POOL  # 导入我们创建的数据库连接池包


def get_info():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4209.400'
    }
    res = requests.get('https://chp.shadiao.app/api.php', headers=header).text
    res = res.replace('\n', '')  # 处理
    if '--' in res:
        res = res[:res.index('——')].strip()
    res = res + '    ——for mingbo'
    return res


# 打开连接
def create_conn():
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    return conn, cursor


# 关闭连接
def close_conn(conn, cursor):
    cursor.close()
    conn.close()


# 插入一条数据
def insert(sql):
    conn, cursor = create_conn()
    res = cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)
    return res


# sql = "insert into users(name,age) VALUES (%s, %s)"

# insert(sql,("mjj",9))


if __name__ == '__main__':
    i = 0
    while i < 1000:
        res = get_info()
        i += 1
        try:
            sql = 'insert into caihongpi values ({},"{}");'.format(i, res)
            print(sql)
            insert(sql)
            time.sleep(0.3)
        except:
            pass
