import sys
import typing as t
from functools import update_wrapper
from types import TracebackType

from werkzeug.exceptions import HTTPException

from .globals import _app_ctx_stack
from .globals import _request_ctx_stack
from .signals import appcontext_popped
from .signals import appcontext_pushed
from .typing import AfterRequestCallable

if t.TYPE_CHECKING:
    from .app import Flask
    from .sessions import SessionMixin
    from .wrappers import Request

# a singleton sentinel value for parameter defaults
_sentinel = object()


class _AppCtxGlobals:
    """A plain object. Used as a namespace for storing data during an
    application context.

    Creating an app context automatically creates this object, which is
    made available as the :data:`g` proxy.

    .. describe:: 'key' in g

        Check whether an attribute is present.

        .. versionadded:: 0.10

    .. describe:: iter(g)

        Return an iterator over the attribute names.

        .. versionadded:: 0.10
    """

    # Define attr methods to let mypy know this is a namespace object
    # that has arbitrary attributes.

    def __getattr__(self, name: str) -> t.Any:
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name) from None

    def __setattr__(self, name: str, value: t.Any) -> None:
        self.__dict__[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self.__dict__[name]
        except KeyError:
            raise AttributeError(name) from None

    def get(self, name: str, default: t.Optional[t.Any] = None) -> t.Any:
        """Get an attribute by name, or a default value. Like
        :meth:`dict.get`.

        :param name: Name of attribute to get.
        :param default: Value to return if the attribute is not present.

        .. versionadded:: 0.10
        """
        return self.__dict__.get(name, default)

    def pop(self, name: str, default: t.Any = _sentinel) -> t.Any:
        """Get and remove an attribute by name. Like :meth:`dict.pop`.

        :param name: Name of attribute to pop.
        :param default: Value to return if the attribute is not present,
            instead of raising a ``KeyError``.

        .. versionadded:: 0.11
        """
        if default is _sentinel:
            return self.__dict__.pop(name)
        else:
            return self.__dict__.pop(name, default)

    def setdefault(self, name: str, default: t.Any = None) -> t.Any:
        """Get the value of an attribute if it is present, otherwise
        set and return a default value. Like :meth:`dict.setdefault`.

        :param name: Name of attribute to get.
        :param default: Value to set and return if the attribute is not
            present.

        .. versionadded:: 0.11
        """
        return self.__dict__.setdefault(name, default)

    def __contains__(self, item: str) -> bool:
        return item in self.__dict__

    def __iter__(self) -> t.Iterator[str]:
        return iter(self.__dict__)

    def __repr__(self) -> str:
        top = _app_ctx_stack.top
        if top is not None:
            return f"<flask.g of {top.app.name!r}>"
        return object.__repr__(self)


def after_this_request(f: AfterRequestCallable) -> AfterRequestCallable:
    """Executes a function after this request.  This is useful to modify
    response objects.  The function is passed the response object and has
    to return the same or a new one.

    Example::

        @app.route('/')
        def index():
            @after_this_request
            def add_header(response):
                response.headers['X-Foo'] = 'Parachute'
                return response
            return 'Hello World!'

    This is more useful if a function other than the view function wants to
    modify a response.  For instance think of a decorator that wants to add
    some headers without converting the return value into a response object.

    .. versionadded:: 0.9
    """
    _request_ctx_stack.top._after_request_functions.append(f)
    return f


def copy_current_request_context(f: t.Callable) -> t.Callable:
    """A helper function that decorates a function to retain the current
    request context.  This is useful when working with greenlets.  The moment
    the function is decorated a copy of the request context is created and
    then pushed when the function is called.  The current session is also
    included in the copied request context.

    Example::

        import gevent
        from flask import copy_current_request_context

        @app.route('/')
        def index():
            @copy_current_request_context
            def do_some_work():
                # do some work here, it can access flask.request or
                # flask.session like you would otherwise in the view function.
                ...
            gevent.spawn(do_some_work)
            return 'Regular response'

    .. versionadded:: 0.10
    """
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(
            "This decorator can only be used at local scopes "
            "when a request context is on the stack.  For instance within "
            "view functions."
        )
    reqctx = top.copy()

    def wrapper(*args, **kwargs):
        with reqctx:
            return f(*args, **kwargs)

    return update_wrapper(wrapper, f)


def has_request_context() -> bool:
    """If you have code that wants to test if a request context is there or
    not this function can be used.  For instance, you may want to take advantage
    of request information if the request object is available, but fail
    silently if it is unavailable.

    ::

        class User(db.Model):

            def __init__(self, username, remote_addr=None):
                self.username = username
                if remote_addr is None and has_request_context():
                    remote_addr = request.remote_addr
                self.remote_addr = remote_addr

    Alternatively you can also just test any of the context bound objects
    (such as :class:`request` or :class:`g`) for truthness::

        class User(db.Model):

            def __init__(self, username, remote_addr=None):
                self.username = username
                if remote_addr is None and request:
                    remote_addr = request.remote_addr
                self.remote_addr = remote_addr

    .. versionadded:: 0.7
    """
    return _request_ctx_stack.top is not None


def has_app_context() -> bool:
    """Works like :func:`has_request_context` but for the application
    context.  You can also just do a boolean check on the
    :data:`current_app` object instead.

    .. versionadded:: 0.9
    """
    return _app_ctx_stack.top is not None


class AppContext:
    """应用上下文（Application Context）将应用对象隐式地绑定到当前线程或greenlet上，类似于请求上下文（Request Context）绑定请求信息的方式。
    如果创建了请求上下文但没有创建应用上下文，那么应用上下文也会被隐式地创建。
    应用上下文的作用是提供一个容器来保存应用级别的状态和配置信息，例如应用的配置参数、数据库连接等。它可以在整个应用程序范围内访问和共享这些数据，而不局限于单个请求。

    当处理请求时，应用上下文会自动创建，并且与当前的请求上下文相关联。这样，您可以在视图函数中访问应用上下文，以获取应用级别的数据。
    使用应用上下文可以确保应用对象在线程或greenlet范围内的唯一性，并提供一个可靠的方式来访问应用级别的数据，以便更好地管理和共享应用的状态和配置信息。
    """

    def __init__(self, app: "Flask") -> None:
        self.app = app
        self.url_adapter = app.create_url_adapter(None)
        self.g = app.app_ctx_globals_class()

        # 与请求上下文一样，应用程序上下文可以多次推送，但基本的“引用计数”足以跟踪它们。
        self._refcnt = 0

    def push(self) -> None:
        """将应用程序上下文绑定到当前上下文。"""
        self._refcnt += 1
        _app_ctx_stack.push(self)
        appcontext_pushed.send(self.app)

    def pop(self, exc: t.Optional[BaseException] = _sentinel) -> None:  # type: ignore
        """Pops the app context."""
        try:
            self._refcnt -= 1
            if self._refcnt <= 0:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_appcontext(exc)
        finally:
            rv = _app_ctx_stack.pop()
        assert rv is self, f"Popped wrong app context.  ({rv!r} instead of {self!r})"
        appcontext_popped.send(self.app)

    def __enter__(self) -> "AppContext":
        self.push()
        return self

    def __exit__(
            self, exc_type: type, exc_value: BaseException, tb: TracebackType
    ) -> None:
        self.pop(exc_value)


class RequestContext:
    """请求上下文（Request Context）包含所有与请求相关的信息。它在请求开始时创建，并被推送到`_request_ctx_stack`栈中，在请求结束时被移除。
    请求上下文会创建URL适配器（URL adapter）和请求对象（request object），用于处理提供的WSGI环境。

    请勿直接使用此类，而是使用`flask.Flask.test_request_context`和`flask.Flask.request_context`方法来创建该对象。
    当请求上下文被弹出时，它将评估应用程序上注册的所有“拆卸处理函数”（teardown function）（`flask.Flask.teardown_request`）进行执行。
    请求上下文会在请求结束时自动弹出。在调试模式下，如果发生异常，请求上下文将保留下来，以便交互式调试器有机会检查数据。从0.4版本开始，这也可以在没有发生异常且不处于`DEBUG`模式下强制执行。通过在WSGI环境中将`'flask._preserve_context'`设置为`True`，上下文将不会在请求结束时自动弹出。例如，`flask.Flask.test_client`方法使用这种方式来实现延迟清理功能。
    在单元测试中，您可能会发现这对于需要更长时间保留上下文本地信息很有帮助。确保在这种情况下正确地使用`werkzeug.LocalStack.pop`方法弹出栈，否则您的单元测试可能会导致内存泄漏。
    """

    def __init__(
            self,
            app: "Flask",
            environ: dict,
            request: t.Optional["Request"] = None,
            session: t.Optional["SessionMixin"] = None,
    ) -> None:
        self.app = app
        if request is None:
            request = app.request_class(environ)  # 创建了一个Request对象
        self.request = request  # app.request_class就是Flask.request_class
        self.url_adapter = None
        try:
            self.url_adapter = app.create_url_adapter(self.request)
        except HTTPException as e:
            self.request.routing_exception = e
        self.flashes = None
        self.session = session

        # 请求上下文可以被多次推送，并且可以与其他请求上下文交错使用。
        # 只有当最后一个请求上下文被弹出时，Flask 才会将它们清除掉。
        # 如果应用上下文缺失，Flask 会隐式地创建一个应用上下文
        self._implicit_app_ctx_stack: t.List[t.Optional["AppContext"]] = []

        # 指示上下文是否被保留。 下次推送另一个上下文时，会弹出保留的上下文。
        self.preserved = False

        # 记住 pop 的例外情况（如果有），以防上下文保留启动。
        self._preserved_exc = None

        # 应在响应对象上发出请求后执行的函数。 这些将在常规“after_request”函数之前调用。
        self._after_request_functions: t.List[AfterRequestCallable] = []

    @property
    def g(self) -> AppContext:
        return _app_ctx_stack.top.g

    @g.setter
    def g(self, value: AppContext) -> None:
        _app_ctx_stack.top.g = value

    def copy(self) -> "RequestContext":
        """Creates a copy of this request context with the same request object.
        This can be used to move a request context to a different greenlet.
        Because the actual request object is the same this cannot be used to
        move a request context to a different thread unless access to the
        request object is locked.

        .. versionadded:: 0.10

        .. versionchanged:: 1.1
           The current session object is used instead of reloading the original
           data. This prevents `flask.session` pointing to an out-of-date object.
        """
        return self.__class__(
            self.app,
            environ=self.request.environ,
            request=self.request,
            session=self.session,
        )

    def match_request(self) -> None:
        """Can be overridden by a subclass to hook into the matching
        of the request.
        """
        try:
            result = self.url_adapter.match(return_rule=True)  # type: ignore
            self.request.url_rule, self.request.view_args = result  # type: ignore
        except HTTPException as e:
            self.request.routing_exception = e

    def push(self) -> None:
        """将请求上下文绑定到当前上下文。"""
        top = _request_ctx_stack.top
        if top is not None and top.preserved:
            top.pop(top._preserved_exc)

        # 在推送请求上下文之前，必须确保存在应用上下文。
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)
        else:
            self._implicit_app_ctx_stack.append(None)

        _request_ctx_stack.push(self)

        # Open the session at the moment that the request context is available.
        # This allows a custom open_session method to use the request context.
        # Only open a new session if this is the first time the request was
        # pushed, otherwise stream_with_context loses the session.
        if self.session is None:
            session_interface = self.app.session_interface
            self.session = session_interface.open_session(self.app, self.request)

            if self.session is None:
                self.session = session_interface.make_null_session(self.app)

        # Match the request URL after loading the session, so that the
        # session is available in custom URL converters.
        if self.url_adapter is not None:
            self.match_request()

    def pop(self, exc: t.Optional[BaseException] = _sentinel) -> None:  # type: ignore
        """
        弹出请求上下文并通过这样做解除绑定。 这还将触发由 teardown_request 装饰器注册的函数的执行。
        """
        app_ctx = self._implicit_app_ctx_stack.pop()
        clear_request = False

        try:
            if not self._implicit_app_ctx_stack:
                self.preserved = False
                self._preserved_exc = None
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_request(exc)

                request_close = getattr(self.request, "close", None)
                if request_close is not None:
                    request_close()
                clear_request = True
        finally:
            rv = _request_ctx_stack.pop()

            # get rid of circular dependencies at the end of the request
            # so that we don't require the GC to be active.
            if clear_request:
                rv.request.environ["werkzeug.request"] = None

            # Get rid of the app as well if necessary.
            if app_ctx is not None:
                app_ctx.pop(exc)

            assert (
                    rv is self
            ), f"Popped wrong request context. ({rv!r} instead of {self!r})"

    def auto_pop(self, exc: t.Optional[BaseException]) -> None:
        if self.request.environ.get("flask._preserve_context") or (
                exc is not None and self.app.preserve_context_on_exception
        ):
            self.preserved = True
            self._preserved_exc = exc  # type: ignore
        else:
            self.pop(exc)

    def __enter__(self) -> "RequestContext":
        self.push()
        return self

    def __exit__(
            self, exc_type: type, exc_value: BaseException, tb: TracebackType
    ) -> None:
        # do not pop the request stack if we are in debug mode and an
        # exception happened.  This will allow the debugger to still
        # access the request object in the interactive shell.  Furthermore
        # the context can be force kept alive for the test client.
        # See flask.testing for how this works.
        self.auto_pop(exc_value)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} {self.request.url!r}"
            f" [{self.request.method}] of {self.app.name}>"
        )
