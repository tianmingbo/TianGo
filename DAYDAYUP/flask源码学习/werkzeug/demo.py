from werkzeug.wrappers import Response, Request


def application(environ, start_response):
    request = Request(environ)
    text = f'Hello {request.args.get("name", "world")}'
    response = Response(text, mimetype='text/plain')
    return response(environ, start_response)
