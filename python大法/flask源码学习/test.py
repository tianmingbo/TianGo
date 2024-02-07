from flask import Flask, request
from werkzeug.local import LocalProxy

app = Flask(__name__)

# 使用 LocalProxy 代理当前请求对象
request_proxy = LocalProxy(lambda: request)


@app.route('/')
def index():
    # 可以直接使用 request_proxy 访问请求对象属性
    user_agent = request_proxy.headers.get('User-Agent')
    return f"User-Agent: {user_agent}"


if __name__ == "__main__":
    app.run()
