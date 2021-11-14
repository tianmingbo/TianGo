# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 9:57
# @Author  : tmb
import requests
import json
from DAYDAYUP.spider.spider_app.douyin.models import session
from DAYDAYUP.spider.spider_app.douyin.models.user_models import UserInfo


def get_homePage_info():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    res = requests.get(
        url='https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=MS4wLjABAAAAX8NIukFGQV1kAtUiP-jkgrT-kYr_xyutgTI1En73l18',
        headers=headers)

    res = json.loads(res.text)
    avatar_image = res['user_info']['avatar_larger']['url_list'][0]
    nickname = res['user_info']['nickname']
    signature = res['user_info']['signature']
    following_count = res['user_info']['following_count']  # 关注
    fans = res['user_info']['follower_count']  # 粉丝
    zan = res['user_info']['total_favorited']  # 赞
    works_count = res['user_info']['aweme_count']  # 作品
    favoriting_count = res['user_info']['favoriting_count']  # 喜欢
    douyin_id = res['user_info']['uid']

    obj = UserInfo(avatar_image=avatar_image,
                   nickname=nickname,
                   signature=signature,
                   following_count=following_count,
                   fans=fans,
                   zan=zan,
                   works_count=works_count,
                   favoriting_count=favoriting_count,
                   douyin_id=douyin_id)
    session.add(obj)
    session.commit()


if __name__ == '__main__':
    get_homePage_info()
