class IPBlacklistMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        ip_addr = environ.get('HTTP_HOST').split(':')[0]
        if ip_addr not in ('127.0.0.1'):
            return forbidden(environ, start_response)

        return self.app(environ, start_response)


def forbidden(environ, start_response):
    print(environ)
    start_response('403 Forbidden', [('Content-Type', 'text/plain')])
    return [b'dsb']


def application(environ, start_response):
    """
    environ: 字典：包含请求的所有信息
    start_response: 在可调用对象中调用的函数，用来发起响应，参数包括状态码，headers等
    """
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'This is a python application!\n']


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    application = IPBlacklistMiddleware(application)
    server = make_server('0.0.0.0', 8999, application)
    server.serve_forever()
