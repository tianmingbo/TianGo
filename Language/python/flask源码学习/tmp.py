import os


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']


def wsgi_server(application):
    environ = dict(os.environ.items())

    def start_response(status, response_headers):
        print(f'status: {status}')
        print(f'response_headers: {response_headers}')

    result = application(environ, start_response)
    for data in result:
        print(f'response_body: {data}')


if __name__ == '__main__':
    wsgi_server(simple_app)
