import requests
from urllib.parse import quote

"""
function main(splash)
    splash:go("https://www.baidu.com")
    input=splash:select("#kw")
    input:send_text('Splash')
    splash:wait(3)
    return splash:png()
  end
"""
"""
mouse_click()

function main(splash)
    splash:go("https://www.baidu.com")
    input=splash:select("#kw")
    input:send_text('Splash')
    splash:wait(3)
  	submit=splash:select('#su')
   	submit.mouse_click()
  splash:wait(5)
    return splash:png()
  end  
"""

# use api

# render.html获取htm源码
# url = 'http://150.158.47.35:8050/render.html?url=https://www.baidu.com&amp:wait=5'
# render.png获取截图
# url = 'http://150.158.47.35:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700'
# render.har 用于获取加载过程中的HAR数据
# url = 'http://150.158.47.35:8050/render.har?url=https://www.jd.com&wait=5'
# res = requests.get(url)
# with open('test.png', 'wb') as f:
#     f.write(res.content)
lua = '''
function main(splash)
    local treat=require("treat")
    local res=splash:http_get("http://www.httpbin.org/get")
    return {html=treat.as_string(res.body),
    url=res.url,
    status=res.status
    }
end
'''
url = 'http://150.158.47.35:8050/execute?lua_source=' + quote(lua)  # 执行lua脚本
res = requests.get(url)
print(res.text)
