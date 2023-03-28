# encoding: utf-8
'''
图片重组
'''
from PIL import Image


def restore_picture(img, imgname):
    img = Image.open(img)
    s = Image.new("RGB", (260, 160))
    ut = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12,
          13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
    height_half = 80
    for inx in range(52):
        c = ut[inx] % 26 * 12 + 1
        u = height_half if ut[inx] > 25 else 0
        l_ = img.crop(box=(c, u, c + 10, u + 80))
        s.paste(l_, box=(inx % 26 * 10, 80 if inx > 25 else 0))
    s.save(f'{imgname}.jpg')
