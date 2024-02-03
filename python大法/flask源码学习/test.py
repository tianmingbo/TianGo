import time

from flask_t import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form.get('message')
        return message
    else:
        time.sleep(10)
        return 'Hello, world!'


if __name__ == '__main__':
    app.run()
