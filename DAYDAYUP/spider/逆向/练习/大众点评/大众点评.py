import re
import json
import requests
import base64
import numpy
from fontTools.ttLib import TTFont  # 处理字体的库
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

with open('dazhongdianping.json', 'r', encoding='utf-8') as f:
    msg = json.load(f)
print(msg)


def font_convert(path):
    font = TTFont(path)  # 打开文件
    font.saveXML('ztiku.xml')
    code_list = font.getGlyphOrder()[2:]
    im = Image.new("RGB", (1800, 1000), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(path, 40)
    count = 15
    array_list = numpy.array_split(code_list, count)  # 将列表切分成15份，以便于在图片上分行显示
    for t in range(count):
        new_list = [i.replace("uni", "\\u") for i in array_list[t]]
        text = "".join(new_list)
        text = text.encode('utf-8').decode('unicode_escape')
        dr.text((0, 50 * t), text, font=font, fill="#000000")

    im.save("s1.jpg")


if __name__ == '__main__':
    font_convert('./zitiku.woff')
