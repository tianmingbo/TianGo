import redis
import os
from werkzeug.urls import url_parse
from werkzeug.wrappers import Request, Response
from werkzeug.middleware.shared_data import SharedDataMiddleware


class Shortly(object):
    def __init__(self, config):
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])

    def dispatch_request(self, request):
        return Response('Hello World!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='loaclhost', redis_port='6379', with_static=True):
    app = Shortly({'redis_host': redis_host,
                   'redis_port': redis_port})
    print(app)
    print(app.wsgi_app)
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                            {'./static': os.path.join(os.path.dirname(__file__), 'static')})
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = create_app()
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
