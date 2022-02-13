import requests
import pytesseract
from PIL import Image

# url = 'http://my.cnki.net/elibregister/CheckCode.aspx'
# res = requests.get(url)
# with open('test1.png', 'wb') as f:
#     f.write(res.content)
image = Image.open('test1.png')
image = image.convert('L')  # 灰度处理
threshold = 120  # 二值化阈值
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
res = pytesseract.image_to_string(image)
print(res)
