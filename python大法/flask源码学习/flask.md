## 2、application context与request context
```
application 指的就是当你调用app = Flask(__name__)创建的这个对象app；
request 指的是每次http请求发生时，WSGI server(比如gunicorn)调用Flask.__call__()之后，在Flask对象内部创建的Request对象；
application 表示用于响应WSGI请求的应用本身，request 表示每次http请求；
application的生命周期大于request，一个application存活期间，可能发生多次http请求，所以，也就会有多个request
```