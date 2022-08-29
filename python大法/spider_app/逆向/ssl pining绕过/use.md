frida -U -f com.goldze.mvvmhabit -l hook.js --no-pause
-f传入要处理的App包名
-l传入Hook脚本

Client closed the connection before a request was made. Possibly the SSL certificate was rejected. //App使用了证书绑定技术，主动停止服务