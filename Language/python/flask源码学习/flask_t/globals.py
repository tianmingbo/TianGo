import typing as t
from functools import partial

from werkzeug.local import LocalProxy
from werkzeug.local import LocalStack

if t.TYPE_CHECKING:
    from .app import Flask
    from .ctx import _AppCtxGlobals
    from .sessions import SessionMixin
    from .wrappers import Request

_request_ctx_err_msg = """\
在请求上下文之外工作。
这通常意味着您尝试使用需要活动 HTTP 请求的功能。 有关如何避免此问题的信息，请参阅测试文档.\
"""
_app_ctx_err_msg = """\
在应用程序上下文之外工作。
这通常意味着您尝试使用需要以某种方式与当前应用程序对象交互的功能。 
要解决此问题，请使用 app.app_context() 设置应用程序上下文。 请参阅文档以获取更多信息.\
"""


def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app


# context locals
_request_ctx_stack = LocalStack()  # 线程隔离栈
_app_ctx_stack = LocalStack()
current_app: "Flask" = LocalProxy(_find_app)  # type: ignore
request: "Request" = LocalProxy(partial(_lookup_req_object, "request"))  # type: ignore
# request: "Request" = LocalProxy(lambda: _lookup_req_object("request"))  # type: ignore
session: "SessionMixin" = LocalProxy(partial(_lookup_req_object, "session"))  # type: ignore
g: "_AppCtxGlobals" = LocalProxy(partial(_lookup_app_object, "g"))  # type: ignore
