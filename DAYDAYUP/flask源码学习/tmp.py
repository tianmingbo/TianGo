from local_example import LocalProxy, LocalStack
from functools import partial

_request_ctx_err_msg = """\
Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request.  Consult the documentation on testing for
information about how to avoid this problem.\
"""


def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    # return getattr(top, name)
    return 'test'


_request_ctx_stack = LocalStack()
_request_ctx_stack.push({'request': 'test'})
# _app_ctx_stack = LocalStack()
# current_app: "Flask" = LocalProxy(_find_app)  # type: ignore
request: "Request" = LocalProxy(partial(_lookup_req_object, "request"))  # type: ignore
# session: "SessionMixin" = LocalProxy(  # type: ignore
#     partial(_lookup_req_object, "session")
# )
# g: "_AppCtxGlobals" = LocalProxy(partial(_lookup_app_object, "g"))  # type: ignore
print(request)
