from server import CookieServer
from services.zhihu import ZhihuLoginService

import settings

srv = CookieServer(settings)

#注册需要登录的服务
srv.register(ZhihuLoginService)

#启动cookie服务
print("启动cookie池服务")
srv.start()