"""
https://sh.58.com/searchjob/
字符加密
High logic FontCreator.exe 解密|或则百度在线编辑
"""
import re
import requests
import base64
from fontTools.ttLib import TTFont  # 处理字体的库
from io import BytesIO

headers = {
    'referer': 'https://sh.58.com/searchjob/?param8516=1&param8427=1',
    'cookie': 'f=n; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; myLat=""; myLon=""; id58=sGhVZWG3UgSlAPoaNRMArg==; mcity=sh; f=n; commontopbar_new_city_info=2%7C%E4%B8%8A%E6%B5%B7%7Csh; city=sh; 58home=sh; commontopbar_ipcity=sh%7C%E4%B8%8A%E6%B5%B7%7C0; 58tj_uuid=bb3ad5e1-1237-4da2-8d98-c613926288a7; new_uv=1; utm_source=market; spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT; wmda_uuid=ca785f2e48f7f706777d4aeab49b5582; wmda_new_uuid=1; wmda_session_id_11187958619315=1639404039726-e48e77f2-2fcd-30c1; als=0; xxzl_deviceid=K%2F58EQLs3EXEO%2F%2BpcIxPh0BWYNhBTjBcSLh%2FrN2e3nKuE6BD4nVZ3rL1BfkMCuss; sessionid=3432f1a4-75f5-4807-8e09-1de746cfd9df; param8616=0; param8716kop=1; wmda_session_id_10104579731767=1639404070734-70a12c45-12de-81c1; new_session=0; wmda_session_id_1731916484865=1639404108096-e25c5a69-17ac-05e0; wmda_visited_projects=%3B11187958619315%3B10104579731767%3B1731916484865; fzq_h=e834bf0132f9bd7c502ec410a660216b_1639404124242_e5a182458ded47219399ad1c8fccd06c_1699772603; init_refer=; fzq_js_zhaopin_list_pc=164797c8df90fc22a81a2a920bc723f9_1639404125166_7; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1639404125; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1639404125; www58com="UserID=72215159385618&UserName=iuiealaha"; 58cooper="userid=72215159385618&username=iuiealaha"; 58uname=iuiealaha; passportAccount="atype=0&bstate=0"; xxzl_smartid=f282a359b5234161427aa6a55cf9fdd2; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1639404401; isSmartSortTipShowed=true; ljrzfc=1; PPU="UID=72215159385618&UN=iuiealaha&TT=046460f4b48ad35d4343fe1f2976459e&PBODY=X8eu-V30lqzVl-Bo0ORqRgWaLFbFw_jmdW9K-maRuopApEoXUN1997HdZkdyMzHFgw8k2y5Lfn3lLnLeIbsqcWhahJWkhV68wDT2ZvgrTbSrbNw47sOjFk1FGP25G-Af4gph9ZzGW-yTnBt99qM8ml4DwS6v95gGEB2mqL6GknQ&VER=1&CUID=06Ze5tIJHt-uhnv95r7R2w"; jl_list_left_banner=101; JSESSIONID=8877707FF02687D031E216A75C412B25; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1639404816; xxzl_cid=5f77cf869cdc4564b49e54884221aab5; xzuid=c139adb6-2f67-46af-b5be-be5f21646b95'
}
# url = 'https://sh.58.com/searchjob/?param8516=1'
# res = requests.get(url=url, headers=headers)
with open('tmp.html', 'r', encoding='utf-8') as f:
    res = f.read()
encrypt_re = re.compile('base64,(.*?)\)')
match_encrypt = re.findall(encrypt_re, res)[0]

b = base64.b64decode(match_encrypt)  # 解密
tf = TTFont(BytesIO(b))
with open('ztku01.woff', 'wb') as f:
    f.write(b)
fonts = TTFont('ztku01.woff')
fonts.saveXML('ztiku.xml')  # 保存成xml文件
# print(tf.getGlyphNames())  # 获取unicode编码
"""
接下来的步骤：
可以从high light fontcreator工具中查找字体的编码，
然后去xml文件中定位位置，
发现相同的字的（x2-x1）,(y2-y1)相等，
然后就是根据（x2-x1,y2-y1）:"田" 建立字体库
"""
font_key = {}
data_map = {}  # 坐标对应的字体，需要手动收集
for i in tf.getGlyphNames()[1:-1]:
    print(i)
    tmp = tf['glyf'][i].coordinates
    x1, y1 = tmp[0]  # 获取前两个坐标
    x2, y2 = tmp[1]
    new = (x2 - x1, y2 - y1)  # (x2-x1,y2-y1）:"田" 建立字体库,这个值是不会变化滴
    key = i.replace('uni', '&#x').lower()
    font_key[key] = new
    font = data_map.get('key', '')  # 得到真实字体
    print(new)
print(font_key)
