# mian.py
def application(env, start_response):
    print(env)
    start_response("200 OK", [("Content-Type", "text/html")])
    return [b"WSGI hello!"]
