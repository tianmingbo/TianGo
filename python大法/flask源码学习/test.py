from flask_t import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    # 可以直接使用 request_proxy 访问请求对象属性
    print(request.headers.get('User-Agent'))
    # user_agent = request_proxy.headers.get('User-Agent')
    return f"User-Agent: fafaf"


if __name__ == "__main__":
    app.run()
