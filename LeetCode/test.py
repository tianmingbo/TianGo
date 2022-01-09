import requests

url_svg = 'http://www.porters.vip/confusion/font/food.svg'
url_css = 'http://www.porters.vip/confusion/css/food.css'
css_class_name = 'vhkbvu'
css_resp = requests.get(url_css).text
svg_resp = requests.get(url_svg).text
print(css_resp, svg_resp)
