import copy
import hashlib
import json
import re

import requests
from fontTools.ttLib import TTFont

"""
1:根据首页中的css中，获取其中的woff字体文件。
2：以其中的一个字体文件为例，建立映射关系
    ①uniefba与uniecbf肃然不一样，但是却描述了同一个字符（注意：不能用点的数量来判断是不是描述的同一个字符，只有起止点和点坐标完全一样的，才是描述同一个字符）
	如：
	uniefba：
	<TTGlyph name="uniefba" xMin="0" yMin="-14" xMax="550" yMax="728">
      <contour>
        <pt x="307" y="728" on="1"/>
        <pt x="205" y="728" on="0"/>
        <pt x="142" y="670" on="1"/>
        <pt x="76" y="612" on="0"/>
        <pt x="66" y="508" on="1"/>
        <pt x="147" y="508" on="1"/>
        <pt x="154" y="580" on="0"/>
        <pt x="236" y="658" on="0"/>
		...
        <pt x="418" y="374" on="1"/>
        <pt x="535" y="414" on="0"/>
        <pt x="535" y="534" on="1"/>
        <pt x="535" y="624" on="0"/>
        <pt x="410" y="728" on="0"/>
      </contour>
      <instructions/>
    </TTGlyph>
	
	uniecbf：
	    <TTGlyph name="uniecbf" xMin="0" yMin="-14" xMax="550" yMax="728">
      <contour>
        <pt x="307" y="728" on="1"/>
        <pt x="205" y="728" on="0"/>
        <pt x="142" y="670" on="1"/>
        <pt x="76" y="612" on="0"/>
        <pt x="66" y="508" on="1"/>
        <pt x="147" y="508" on="1"/>
        <pt x="154" y="580" on="0"/>
        <pt x="236" y="658" on="0"/>
        <pt x="308" y="657" on="1"/>
        <pt x="378" y="658" on="0"/>
		...
        <pt x="481" y="355" on="0"/>
        <pt x="418" y="374" on="1"/>
        <pt x="535" y="414" on="0"/>
        <pt x="535" y="534" on="1"/>
        <pt x="535" y="624" on="0"/>
        <pt x="410" y="728" on="0"/>
      </contour>
      <instructions/>
    </TTGlyph>
	两者的内容是完全一样的，所以是描述同一个字符。
	知道了这个方法，那么如何建立映射？
	
	可以以字形数据建立映射：{'name':['uniefba','uniecbf'],'value':'0','hex':md5(content)} #因为字形数据多，以MD5值来区分唯一值,
	选择一个woff文件，
"""


# 访问页面需要验证，重点不在这里，直接拿到css文件，匹配里面的woff
# headers = {
#     'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
# }
#
# resp = requests.get('https://www.dianping.com/shop/G4mmqiZrzgkpQZGY', headers=headers)
# print(resp.text)

def get_mapping():
    with open('load.css', 'r') as f:
        css = f.read()
    with open('word.txt', 'r', encoding='utf-8') as f:
        word = f.read()
    mapping = {}

    woff_link = re.findall(re.compile(r',url\("(.*)\.woff"\);'), css)
    woff_link = ['https:' + i + '.woff' for i in list(set(woff_link))]
    for i in range(len(woff_link)):
        res = requests.get(woff_link[i])
        with open(f'{i}.woff', 'wb') as f:
            f.write(res.content)
        font = TTFont(f'{i}.woff')
        content = font.getGlyphOrder()[2:]
        for j in range(len(content)):
            md5_value = hashlib.md5(font['glyf'].glyphs.get(content[j]).data).hexdigest()
            if md5_value not in mapping:
                mapping[md5_value] = {'name': {content[j]}, 'value': word[j]}
            else:
                mapping[md5_value]['name'].add(content[j])
    return mapping


def get_value(i, mapping):
    for k, v in mapping.items():
        if i in v['name']:
            return v['value']
    return i


def process(mapping):
    with open('dazhongdianping.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())
    test_str = info['reviewAllDOList'][0]['reviewDataVO']['reviewBody']
    print(test_str)
    res = re.sub('<svgmtsi class=\\"review\\">', '', test_str)
    res = re.sub(';</svgmtsi>', '', res)
    res = re.sub('<.*?>', '', res)
    res = res.replace('&#x', 'uni')
    wait_replace = re.findall(re.compile(r'uni[0-9a-z]{4}'), res)
    for i in wait_replace:
        res = res.replace(i, get_value(i, mapping))
    return res


if __name__ == '__main__':
    mapping = get_mapping()
    res = process(mapping)
    print(res)