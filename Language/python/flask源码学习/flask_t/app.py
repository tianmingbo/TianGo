import functools
import inspect
import logging
import os
import sys
import typing as t
import weakref
from datetime import timedelta
from itertools import chain
from threading import Lock
from types import TracebackType

from werkzeug.datastructures import Headers
from werkzeug.datastructures import ImmutableDict
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import InternalServerError
from werkzeug.local import ContextVar
from werkzeug.routing import BuildError
from werkzeug.routing import Map
from werkzeug.routing import MapAdapter
from werkzeug.routing import RequestRedirect
from werkzeug.routing import RoutingException
from werkzeug.routing import Rule
from werkzeug.wrappers import Response as BaseResponse

from . import cli
from . import json
from .config import Config
from .config import ConfigAttribute
from .ctx import _AppCtxGlobals
from .ctx import AppContext
from .ctx import RequestContext
from .globals import _request_ctx_stack
from .globals import g
from .globals import request
from .globals import session
from .helpers import _split_blueprint_path
from .helpers import get_debug_flag
from .helpers import get_env
from .helpers import get_flashed_messages
from .helpers import get_load_dotenv
from .helpers import locked_cached_property
from .helpers import url_for
from .json import jsonify
from .logging import create_logger
from .scaffold import _endpoint_from_view_func
from .scaffold import _sentinel
from .scaffold import find_package
from .scaffold import Scaffold
from .scaffold import setupmethod
from .sessions import SecureCookieSessionInterface
from .signals import appcontext_tearing_down
from .signals import got_request_exception
from .signals import request_finished
from .signals import request_started
from .signals import request_tearing_down
from .templating import DispatchingJinjaLoader
from .templating import Environment
from .typing import AfterRequestCallable
from .typing import BeforeRequestCallable
from .typing import ErrorHandlerCallable
from .typing import ResponseReturnValue
from .typing import TeardownCallable
from .typing import TemplateContextProcessorCallable
from .typing import TemplateFilterCallable
from .typing import TemplateGlobalCallable
from .typing import TemplateTestCallable
from .typing import URLDefaultCallable
from .typing import URLValuePreprocessorCallable
from .wrappers import Request
from .wrappers import Response

if t.TYPE_CHECKING:
    import typing_extensions as te
    from .blueprints import Blueprint
    from .testing import FlaskClient
    from .testing import FlaskCliRunner

if sys.version_info >= (3, 8):
    iscoroutinefunction = inspect.iscoroutinefunction
else:

    def iscoroutinefunction(func: t.Any) -> bool:
        while inspect.ismethod(func):
            func = func.__func__

        while isinstance(func, functools.partial):
            func = func.func

        return inspect.iscoroutinefunction(func)


def _make_timedelta(value: t.Optional[timedelta]) -> t.Optional[timedelta]:
    if value is None or isinstance(value, timedelta):
        return value

    return timedelta(seconds=value)


class Flask(Scaffold):
    """
    import_name：应用程序包的名称，用于定位文件系统上的资源，也可供扩展使用以改进调试信息等。
    static_url_path：用于指定 Web 上静态文件的不同路径，默认为static_folder文件夹的名称。
    static_folder：包含在static_url_path下提供服务的静态文件的文件夹，默认为'static'。
    static_host：在添加静态路由时要使用的主机，默认为None。在使用host_matching=True和配置了static_folder时需要设置。
    host_matching：设置url_map.host_matching属性，默认为False。
    subdomain_matching：在匹配路由时考虑相对于SERVER_NAME的子域，默认为False。
    template_folder：包含应用程序应使用的模板的文件夹，默认为应用程序根路径中的'templates'文件夹。
    instance_path：应用程序的替代实例路径，默认为假设在包或模块旁边的'instance'文件夹。
    instance_relative_config：如果设置为True，则假定用于加载配置的相对文件名与实例路径相关，而不是应用程序根路径相关。
    root_path：应用程序文件根路径的路径。只有在无法自动检测时才应手动设置，例如用于命名空间包。
    """

    # 请求类
    request_class = Request

    # 响应类
    response_class = Response

    # The class that is used for the Jinja environment.
    #
    # .. versionadded:: 0.11
    jinja_environment = Environment

    # 用于实现g全局属性
    app_ctx_globals_class = _AppCtxGlobals

    # 配置类
    config_class = Config

    # The testing flag.  Set this to ``True`` to enable the test mode of
    # Flask extensions (and in the future probably also Flask itself).
    # For example this might activate test helpers that have an
    # additional runtime cost which should not be enabled by default.
    #
    # If this is enabled and PROPAGATE_EXCEPTIONS is not changed from the
    # default it's implicitly enabled.
    #
    # This attribute can also be configured from the config with the
    # ``TESTING`` configuration key.  Defaults to ``False``.
    testing = ConfigAttribute("TESTING")

    # secret_key
    secret_key = ConfigAttribute("SECRET_KEY")

    # session名字，默认为session
    session_cookie_name = ConfigAttribute("SESSION_COOKIE_NAME")

    # session过期时间，默认31天
    permanent_session_lifetime = ConfigAttribute(
        "PERMANENT_SESSION_LIFETIME", get_converter=_make_timedelta
    )

    # 设置使用send_file函数时的默认max_age参数。max_age用于设置文件缓存的最大时长，即文件在浏览器端的缓存时间。
    # 默认的max_age设置为None，服务器会检查文件是否有更新，如果没有更新，则返回一个304 Not Modified响应，告诉浏览器继续使用缓存的文件。
    send_file_max_age_default = ConfigAttribute(
        "SEND_FILE_MAX_AGE_DEFAULT", get_converter=_make_timedelta
    )

    # use_x_sendfile 为 True 时，应用程序可以利用服务器的 X-Sendfile 功能。
    # 使用 X-Sendfile，应用程序只需将文件路径发送给服务器，然后服务器会负责将文件发送给客户端。
    use_x_sendfile = ConfigAttribute("USE_X_SENDFILE")

    json_encoder = json.JSONEncoder
    json_decoder = json.JSONDecoder

    # Options that are passed to the Jinja environment in
    # :meth:`create_jinja_environment`. Changing these options after
    # the environment is created (accessing :attr:`jinja_env`) will
    # have no effect.
    #
    # .. versionchanged:: 1.1.0
    #     This is a ``dict`` instead of an ``ImmutableDict`` to allow
    #     easier configuration.
    #
    jinja_options: dict = {}

    # Default configuration parameters.
    default_config = ImmutableDict(
        {
            "ENV": None,
            "DEBUG": None,
            "TESTING": False,
            "PROPAGATE_EXCEPTIONS": None,
            "PRESERVE_CONTEXT_ON_EXCEPTION": None,
            "SECRET_KEY": None,
            "PERMANENT_SESSION_LIFETIME": timedelta(days=31),
            "USE_X_SENDFILE": False,
            "SERVER_NAME": None,
            "APPLICATION_ROOT": "/",
            "SESSION_COOKIE_NAME": "session",
            "SESSION_COOKIE_DOMAIN": None,
            "SESSION_COOKIE_PATH": None,
            "SESSION_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SECURE": False,
            "SESSION_COOKIE_SAMESITE": None,
            "SESSION_REFRESH_EACH_REQUEST": True,
            "MAX_CONTENT_LENGTH": None,
            "SEND_FILE_MAX_AGE_DEFAULT": None,
            "TRAP_BAD_REQUEST_ERRORS": None,
            "TRAP_HTTP_EXCEPTIONS": False,
            "EXPLAIN_TEMPLATE_LOADING": False,
            "PREFERRED_URL_SCHEME": "http",
            "JSON_AS_ASCII": True,
            "JSON_SORT_KEYS": True,
            "JSONIFY_PRETTYPRINT_REGULAR": False,
            "JSONIFY_MIMETYPE": "application/json",
            "TEMPLATES_AUTO_RELOAD": None,
            "MAX_COOKIE_SIZE": 4093,
        }
    )

    # 用于创建 URL 规则的规则对象。默认为werkzeug.routing.Rule。
    url_rule_class = Rule

    # 用于存储 URL 规则和路由配置参数的映射对象。 默认为werkzeug.routing.Map。
    url_map_class = Map

    # the test client that is used with when `test_client` is used.
    #
    # .. versionadded:: 0.7
    test_client_class: t.Optional[t.Type["FlaskClient"]] = None

    # The :class:`~click.testing.CliRunner` subclass, by default
    # :class:`~flask.testing.FlaskCliRunner` that is used by
    # :meth:`test_cli_runner`. Its ``__init__`` method should take a
    # Flask app object as the first argument.
    #
    # .. versionadded:: 1.0
    test_cli_runner_class: t.Optional[t.Type["FlaskCliRunner"]] = None

    # session类
    session_interface = SecureCookieSessionInterface()

    def __init__(
            self,
            import_name: str,
            static_url_path: t.Optional[str] = None,
            static_folder: t.Optional[str] = "static",
            static_host: t.Optional[str] = None,
            host_matching: bool = False,
            subdomain_matching: bool = False,
            template_folder: t.Optional[str] = "templates",
            instance_path: t.Optional[str] = None,
            instance_relative_config: bool = False,
            root_path: t.Optional[str] = None,
    ):
        super().__init__(
            import_name=import_name,
            static_folder=static_folder,
            static_url_path=static_url_path,
            template_folder=template_folder,
            root_path=root_path,
        )

        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError(
                "If an instance path is provided it must be absolute."
                " A relative path was given instead."
            )

        # 保存instance目录
        self.instance_path = instance_path

        # 加载配置，支持从文件加载
        self.config = self.make_config(instance_relative_config)

        # 路由绑定时错误处理
        self.url_build_error_handlers: t.List[
            t.Callable[[Exception, str, dict], str]
        ] = []

        # 钩子函数
        self.before_first_request_funcs: t.List[BeforeRequestCallable] = []
        self.teardown_appcontext_funcs: t.List[TeardownCallable] = []

        # 创建 shell 上下文时应运行的 shell 上下文处理器函数列表。
        self.shell_context_processors: t.List[t.Callable[[], t.Dict[str, t.Any]]] = []

        # 将注册的蓝图名称映射到蓝图对象。 该字典保留蓝图注册的顺序。蓝图可以多次注册，该字典不跟踪它们附加的频率。
        self.blueprints: t.Dict[str, "Blueprint"] = {}
        # 扩展
        self.extensions: dict = {}

        # 在创建类之后但在连接任何路由之前使用它来更改路由转换器。 Example::
        #
        #    from werkzeug.routing import BaseConverter
        #
        #    class ListConverter(BaseConverter):
        #        def to_python(self, value):
        #            return value.split(',')
        #        def to_url(self, values):
        #            return ','.join(super(ListConverter, self).to_url(value)
        #                            for value in values)
        #
        #    app = Flask(__name__)
        #    app.url_map.converters['list'] = ListConverter
        self.url_map = self.url_map_class()

        self.url_map.host_matching = host_matching
        self.subdomain_matching = subdomain_matching

        # 在内部跟踪应用程序是否已处理至少一个请求。
        self._got_first_request = False
        self._before_request_lock = Lock()

        # 处理静态文件
        if self.has_static_folder:
            assert (
                    bool(static_host) == host_matching
            ), "Invalid static_host/host_matching combination"
            # 使用weakref来避免在应用程序和视图函数之间创建引用循环
            self_ref = weakref.ref(self)
            self.add_url_rule(
                f"{self.static_url_path}/<path:filename>",
                endpoint="static",
                host=static_host,
                view_func=lambda **kw: self_ref().send_static_file(**kw),  # type: ignore # noqa: B950
            )

        # Set the name of the Click group in case someone wants to add
        # the app's commands to another CLI tool.
        self.cli.name = self.name

    def _is_setup_finished(self) -> bool:
        return self.debug and self._got_first_request

    @locked_cached_property
    def name(self) -> str:  # type: ignore
        """
        app name
        """
        if self.import_name == "__main__":
            fn = getattr(sys.modules["__main__"], "__file__", None)
            if fn is None:
                return "__main__"
            return os.path.splitext(os.path.basename(fn))[0]
        return self.import_name

    @property
    def propagate_exceptions(self) -> bool:
        """Returns the value of the ``PROPAGATE_EXCEPTIONS`` configuration
        value in case it's set, otherwise a sensible default is returned.

        .. versionadded:: 0.7
        """
        rv = self.config["PROPAGATE_EXCEPTIONS"]
        if rv is not None:
            return rv
        return self.testing or self.debug

    @property
    def preserve_context_on_exception(self) -> bool:
        """Returns the value of the ``PRESERVE_CONTEXT_ON_EXCEPTION``
        configuration value in case it's set, otherwise a sensible default
        is returned.

        .. versionadded:: 0.7
        """
        rv = self.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
        if rv is not None:
            return rv
        return self.debug

    @locked_cached_property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app, with
        the same name as :attr:`name`.

        In debug mode, the logger's :attr:`~logging.Logger.level` will
        be set to :data:`~logging.DEBUG`.

        If there are no handlers configured, a default handler will be
        added. See :doc:`/logging` for more information.

        .. versionchanged:: 1.1.0
            The logger takes the same name as :attr:`name` rather than
            hard-coding ``"flask.app"``.

        .. versionchanged:: 1.0.0
            Behavior was simplified. The logger is always named
            ``"flask.app"``. The level is only set during configuration,
            it doesn't check ``app.debug`` each time. Only one format is
            used, not different ones depending on ``app.debug``. No
            handlers are removed, and a handler is only added if no
            handlers are already configured.

        .. versionadded:: 0.3
        """
        return create_logger(self)

    @locked_cached_property
    def jinja_env(self) -> Environment:
        """The Jinja environment used to load templates.

        The environment is created the first time this property is
        accessed. Changing :attr:`jinja_options` after that will have no
        effect.
        """
        return self.create_jinja_environment()

    @property
    def got_first_request(self) -> bool:
        """This attribute is set to ``True`` if the application started
        handling the first request.

        .. versionadded:: 0.8
        """
        return self._got_first_request

    def make_config(self, instance_relative: bool = False) -> Config:
        """Used to create the config attribute by the Flask constructor.
        The `instance_relative` parameter is passed in from the constructor
        of Flask (there named `instance_relative_config`) and indicates if
        the config should be relative to the instance path or the root path
        of the application.

        .. versionadded:: 0.8
        """
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        defaults = dict(self.default_config)
        defaults["ENV"] = get_env()
        defaults["DEBUG"] = get_debug_flag()
        return self.config_class(root_path, defaults)

    def auto_find_instance_path(self) -> str:
        """Tries to locate the instance path if it was not provided to the
        constructor of the application class.  It will basically calculate
        the path to a folder named ``instance`` next to your main file or
        the package.

        .. versionadded:: 0.8
        """
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path, "instance")
        return os.path.join(prefix, "var", f"{self.name}-instance")

    def open_instance_resource(self, resource: str, mode: str = "rb") -> t.IO[t.AnyStr]:
        """Opens a resource from the application's instance folder
        (:attr:`instance_path`).  Otherwise works like
        :meth:`open_resource`.  Instance resources can also be opened for
        writing.

        :param resource: the name of the resource.  To access resources within
                         subfolders use forward slashes as separator.
        :param mode: resource file opening mode, default is 'rb'.
        """
        return open(os.path.join(self.instance_path, resource), mode)

    @property
    def templates_auto_reload(self) -> bool:
        """Reload templates when they are changed. Used by
        :meth:`create_jinja_environment`.

        This attribute can be configured with :data:`TEMPLATES_AUTO_RELOAD`. If
        not set, it will be enabled in debug mode.

        .. versionadded:: 1.0
            This property was added but the underlying config and behavior
            already existed.
        """
        rv = self.config["TEMPLATES_AUTO_RELOAD"]
        return rv if rv is not None else self.debug

    @templates_auto_reload.setter
    def templates_auto_reload(self, value: bool) -> None:
        self.config["TEMPLATES_AUTO_RELOAD"] = value

    def create_jinja_environment(self) -> Environment:
        """Create the Jinja environment based on :attr:`jinja_options`
        and the various Jinja-related methods of the app. Changing
        :attr:`jinja_options` after this will have no effect. Also adds
        Flask-related globals and filters to the environment.

        .. versionchanged:: 0.11
           ``Environment.auto_reload`` set in accordance with
           ``TEMPLATES_AUTO_RELOAD`` configuration option.

        .. versionadded:: 0.5
        """
        options = dict(self.jinja_options)

        if "autoescape" not in options:
            options["autoescape"] = self.select_jinja_autoescape

        if "auto_reload" not in options:
            options["auto_reload"] = self.templates_auto_reload

        rv = self.jinja_environment(self, **options)
        rv.globals.update(
            url_for=url_for,
            get_flashed_messages=get_flashed_messages,
            config=self.config,
            # request, session and g are normally added with the
            # context processor for efficiency reasons but for imported
            # templates we also want the proxies in there.
            request=request,
            session=session,
            g=g,
        )
        rv.policies["json.dumps_function"] = json.dumps
        return rv

    def create_global_jinja_loader(self) -> DispatchingJinjaLoader:
        """Creates the loader for the Jinja2 environment.  Can be used to
        override just the loader and keeping the rest unchanged.  It's
        discouraged to override this function.  Instead one should override
        the :meth:`jinja_loader` function instead.

        The global loader dispatches between the loaders of the application
        and the individual blueprints.

        .. versionadded:: 0.7
        """
        return DispatchingJinjaLoader(self)

    def select_jinja_autoescape(self, filename: str) -> bool:
        """Returns ``True`` if autoescaping should be active for the given
        templates name. If no templates name is given, returns `True`.

        .. versionadded:: 0.5
        """
        if filename is None:
            return True
        return filename.endswith((".html", ".htm", ".xml", ".xhtml"))

    def update_template_context(self, context: dict) -> None:
        """Update the templates context with some commonly used variables.
        This injects request, session, config and g into the templates
        context as well as everything templates context processors want
        to inject.  Note that the as of Flask 0.6, the original values
        in the context will not be overridden if a context processor
        decides to return a value with the same key.

        :param context: the context as a dictionary that is updated in place
                        to add extra variables.
        """
        funcs: t.Iterable[
            TemplateContextProcessorCallable
        ] = self.template_context_processors[None]
        reqctx = _request_ctx_stack.top
        if reqctx is not None:
            for bp in request.blueprints:
                if bp in self.template_context_processors:
                    funcs = chain(funcs, self.template_context_processors[bp])
        orig_ctx = context.copy()
        for func in funcs:
            context.update(func())
        # make sure the original values win.  This makes it possible to
        # easier add new variables in context processors without breaking
        # existing views.
        context.update(orig_ctx)

    def make_shell_context(self) -> dict:
        """Returns the shell context for an interactive shell for this
        application.  This runs all the registered shell context
        processors.

        .. versionadded:: 0.11
        """
        rv = {"app": self, "g": g}
        for processor in self.shell_context_processors:
            rv.update(processor())
        return rv

    #: What environment the app is running in. Flask and extensions may
    #: enable behaviors based on the environment, such as enabling debug
    #: mode. This maps to the :data:`ENV` config key. This is set by the
    #: :envvar:`FLASK_ENV` environment variable and may not behave as
    #: expected if set in code.
    #:
    #: **Do not enable development when deploying in production.**
    #:
    #: Default: ``'production'``
    env = ConfigAttribute("ENV")

    @property
    def debug(self) -> bool:
        """Whether debug mode is enabled. When using ``flask run`` to start
        the development server, an interactive debugger will be shown for
        unhandled exceptions, and the server will be reloaded when code
        changes. This maps to the :data:`DEBUG` config key. This is
        enabled when :attr:`env` is ``'development'`` and is overridden
        by the ``FLASK_DEBUG`` environment variable. It may not behave as
        expected if set in code.

        **Do not enable debug mode when deploying in production.**

        Default: ``True`` if :attr:`env` is ``'development'``, or
        ``False`` otherwise.
        """
        return self.config["DEBUG"]

    @debug.setter
    def debug(self, value: bool) -> None:
        self.config["DEBUG"] = value
        self.jinja_env.auto_reload = self.templates_auto_reload

    def run(
            self,
            host: t.Optional[str] = None,
            port: t.Optional[int] = None,
            debug: t.Optional[bool] = None,
            load_dotenv: bool = True,
            **options: t.Any,
    ) -> None:
        """
        load_dotenv:是否加载.env 和 .flaskenv 文件作为环境变量。
        线程模式默认启用。
        """
        # Change this into a no-op if the server is invoked from the
        # command line. Have a look at cli.py for more information.
        if os.environ.get("FLASK_RUN_FROM_CLI") == "true":
            from .debughelpers import explain_ignored_app_run

            explain_ignored_app_run()
            return

        if get_load_dotenv(load_dotenv):
            cli.load_dotenv()

            # if set, let env vars override previous values
            if "FLASK_ENV" in os.environ:
                self.env = get_env()
                self.debug = get_debug_flag()
            elif "FLASK_DEBUG" in os.environ:
                self.debug = get_debug_flag()

        # debug passed to method overrides all other sources
        if debug is not None:
            self.debug = bool(debug)

        server_name = self.config.get("SERVER_NAME")
        sn_host = sn_port = None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        if not host:
            if sn_host:
                host = sn_host
            else:
                host = "127.0.0.1"

        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        options.setdefault("use_reloader", self.debug)
        options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        cli.show_server_banner(self.env, self.debug, self.name, False)

        from werkzeug.serving import run_simple

        try:
            run_simple(t.cast(str, host), port, self, **options)
        finally:
            # reset the first request information if the development server
            # reset normally.  This makes it possible to restart the server
            # without reloader and that stuff from an interactive shell.
            self._got_first_request = False

    def test_client(self, use_cookies: bool = True, **kwargs: t.Any) -> "FlaskClient":
        """Creates a test client for this application.  For information
        about unit testing head over to :doc:`/testing`.

        Note that if you are testing for assertions or exceptions in your
        application code, you must set ``app.testing = True`` in order for the
        exceptions to propagate to the test client.  Otherwise, the exception
        will be handled by the application (not visible to the test client) and
        the only indication of an AssertionError or other exception will be a
        500 status code response to the test client.  See the :attr:`testing`
        attribute.  For example::

            app.testing = True
            client = app.test_client()

        The test client can be used in a ``with`` block to defer the closing down
        of the context until the end of the ``with`` block.  This is useful if
        you want to access the context locals for testing::

            with app.test_client() as c:
                rv = c.get('/?vodka=42')
                assert request.args['vodka'] == '42'

        Additionally, you may pass optional keyword arguments that will then
        be passed to the application's :attr:`test_client_class` constructor.
        For example::

            from flask.testing import FlaskClient

            class CustomClient(FlaskClient):
                def __init__(self, *args, **kwargs):
                    self._authentication = kwargs.pop("authentication")
                    super(CustomClient,self).__init__( *args, **kwargs)

            app.test_client_class = CustomClient
            client = app.test_client(authentication='Basic ....')

        See :class:`~flask.testing.FlaskClient` for more information.

        .. versionchanged:: 0.4
           added support for ``with`` block usage for the client.

        .. versionadded:: 0.7
           The `use_cookies` parameter was added as well as the ability
           to override the client to be used by setting the
           :attr:`test_client_class` attribute.

        .. versionchanged:: 0.11
           Added `**kwargs` to support passing additional keyword arguments to
           the constructor of :attr:`test_client_class`.
        """
        cls = self.test_client_class
        if cls is None:
            from .testing import FlaskClient as cls  # type: ignore
        return cls(  # type: ignore
            self, self.response_class, use_cookies=use_cookies, **kwargs
        )

    def test_cli_runner(self, **kwargs: t.Any) -> "FlaskCliRunner":
        """Create a CLI runner for testing CLI commands.
        See :ref:`testing-cli`.

        Returns an instance of :attr:`test_cli_runner_class`, by default
        :class:`~flask.testing.FlaskCliRunner`. The Flask app object is
        passed as the first argument.

        .. versionadded:: 1.0
        """
        cls = self.test_cli_runner_class

        if cls is None:
            from .testing import FlaskCliRunner as cls  # type: ignore

        return cls(self, **kwargs)  # type: ignore

    @setupmethod
    def register_blueprint(self, blueprint: "Blueprint", **options: t.Any) -> None:
        """Register a :class:`~flask.Blueprint` on the application. Keyword
        arguments passed to this method will override the defaults set on the
        blueprint.

        Calls the blueprint's :meth:`~flask.Blueprint.register` method after
        recording the blueprint in the application's :attr:`blueprints`.

        :param blueprint: The blueprint to register.
        :param url_prefix: Blueprint routes will be prefixed with this.
        :param subdomain: Blueprint routes will match on this subdomain.
        :param url_defaults: Blueprint routes will use these default values for
            view arguments.
        :param options: Additional keyword arguments are passed to
            :class:`~flask.blueprints.BlueprintSetupState`. They can be
            accessed in :meth:`~flask.Blueprint.record` callbacks.

        .. versionchanged:: 2.0.1
            The ``name`` option can be used to change the (pre-dotted)
            name the blueprint is registered with. This allows the same
            blueprint to be registered multiple times with unique names
            for ``url_for``.

        .. versionadded:: 0.7
        """
        blueprint.register(self, options)

    def iter_blueprints(self) -> t.ValuesView["Blueprint"]:
        """Iterates over all blueprints by the order they were registered.

        .. versionadded:: 0.11
        """
        return self.blueprints.values()

    @setupmethod
    def add_url_rule(
            self,
            rule: str,
            endpoint: t.Optional[str] = None,
            view_func: t.Optional[t.Callable] = None,
            provide_automatic_options: t.Optional[bool] = None,
            **options: t.Any,
    ) -> None:
        """
        向应用程序的 URL 映射中添加 URL 规则，并将其与对应的视图函数关联起来
        """
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options["endpoint"] = endpoint
        methods = options.pop("methods", None)

        # 如果没有给出请求方法但是view_func给出，使用view_func的methods属性。
        # 如果两者都不存在，默认使用“GET”。
        if methods is None:
            methods = getattr(view_func, "methods", None) or ("GET",)
        if isinstance(methods, str):
            raise TypeError(
                '允许的方法必须是字符串列表，'
                '例如：@app.route(...,methods=["POST"])'
            )
        methods = {item.upper() for item in methods}

        # Methods that should always be added
        required_methods = set(getattr(view_func, "required_methods", ()))

        # 用于控制是否自动提供 OPTIONS 请求的支持,自动为已添加的 URL 规则提供 OPTIONS 请求的支持，
        # 而无需显式地定义 OPTIONS 请求的处理逻辑。这样做有助于简化跨域请求的处理，因为浏览器在发送复杂的跨域请求时，
        # 会首先发送一个 OPTIONS 请求来检查服务器是否支持实际请求使用的 HTTP 方法
        if provide_automatic_options is None:
            provide_automatic_options = getattr(
                view_func, "provide_automatic_options", None
            )

        if provide_automatic_options is None:
            if "OPTIONS" not in methods:
                provide_automatic_options = True
                required_methods.add("OPTIONS")
            else:
                provide_automatic_options = False

        # Add the required methods now.
        methods |= required_methods

        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options  # type: ignore

        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError(
                    "View function mapping is overwriting an existing"
                    f" endpoint function: {endpoint}"
                )
            self.view_functions[endpoint] = view_func

    @setupmethod
    def template_filter(
            self, name: t.Optional[str] = None
    ) -> t.Callable[[TemplateFilterCallable], TemplateFilterCallable]:
        """A decorator that is used to register custom templates filter.
        You can specify a name for the filter, otherwise the function
        name will be used. Example::

          @app.template_filter()
          def reverse(s):
              return s[::-1]

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """

        def decorator(f: TemplateFilterCallable) -> TemplateFilterCallable:
            self.add_template_filter(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_filter(
            self, f: TemplateFilterCallable, name: t.Optional[str] = None
    ) -> None:
        """Register a custom templates filter.  Works exactly like the
        :meth:`template_filter` decorator.

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """
        self.jinja_env.filters[name or f.__name__] = f

    @setupmethod
    def template_test(
            self, name: t.Optional[str] = None
    ) -> t.Callable[[TemplateTestCallable], TemplateTestCallable]:
        """A decorator that is used to register custom templates test.
        You can specify a name for the test, otherwise the function
        name will be used. Example::

          @app.template_test()
          def is_prime(n):
              if n == 2:
                  return True
              for i in range(2, int(math.ceil(math.sqrt(n))) + 1):
                  if n % i == 0:
                      return False
              return True

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """

        def decorator(f: TemplateTestCallable) -> TemplateTestCallable:
            self.add_template_test(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_test(
            self, f: TemplateTestCallable, name: t.Optional[str] = None
    ) -> None:
        """Register a custom templates test.  Works exactly like the
        :meth:`template_test` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """
        self.jinja_env.tests[name or f.__name__] = f

    @setupmethod
    def template_global(
            self, name: t.Optional[str] = None
    ) -> t.Callable[[TemplateGlobalCallable], TemplateGlobalCallable]:
        """A decorator that is used to register a custom templates global function.
        You can specify a name for the global function, otherwise the function
        name will be used. Example::

            @app.template_global()
            def double(n):
                return 2 * n

        .. versionadded:: 0.10

        :param name: the optional name of the global function, otherwise the
                     function name will be used.
        """

        def decorator(f: TemplateGlobalCallable) -> TemplateGlobalCallable:
            self.add_template_global(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_global(
            self, f: TemplateGlobalCallable, name: t.Optional[str] = None
    ) -> None:
        """Register a custom templates global function. Works exactly like the
        :meth:`template_global` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the global function, otherwise the
                     function name will be used.
        """
        self.jinja_env.globals[name or f.__name__] = f

    @setupmethod
    def before_first_request(self, f: BeforeRequestCallable) -> BeforeRequestCallable:
        """
        注册一个要在第一次请求此应用程序实例之前运行的函数。
        """
        self.before_first_request_funcs.append(f)
        return f

    @setupmethod
    def teardown_appcontext(self, f: TeardownCallable) -> TeardownCallable:
        """注册一个在应用程序上下文结束时调用的函数。
        这些函数通常也会在弹出 requestcontext 时调用

        Example::

            ctx = app.app_context()
            ctx.push()
            ...
            ctx.pop()
        """
        self.teardown_appcontext_funcs.append(f)
        return f

    @setupmethod
    def shell_context_processor(self, f: t.Callable) -> t.Callable:
        """Registers a shell context processor function.

        .. versionadded:: 0.11
        """
        self.shell_context_processors.append(f)
        return f

    def _find_error_handler(self, e: Exception) -> t.Optional[ErrorHandlerCallable]:
        """Return a registered error handler for an exception in this order:
        blueprint handler for a specific code, app handler for a specific code,
        blueprint handler for an exception class, app handler for an exception
        class, or ``None`` if a suitable handler is not found.
        """
        exc_class, code = self._get_exc_class_and_code(type(e))

        for c in [code, None]:
            for name in chain(request.blueprints, [None]):
                handler_map = self.error_handler_spec[name][c]

                if not handler_map:
                    continue

                for cls in exc_class.__mro__:
                    handler = handler_map.get(cls)

                    if handler is not None:
                        return handler
        return None

    def handle_http_exception(
            self, e: HTTPException
    ) -> t.Union[HTTPException, ResponseReturnValue]:
        """Handles an HTTP exception.  By default this will invoke the
        registered error handlers and fall back to returning the
        exception as response.

        .. versionchanged:: 1.0.3
            ``RoutingException``, used internally for actions such as
             slash redirects during routing, is not passed to error
             handlers.

        .. versionchanged:: 1.0
            Exceptions are looked up by code *and* by MRO, so
            ``HTTPExcpetion`` subclasses can be handled with a catch-all
            handler for the base ``HTTPException``.

        .. versionadded:: 0.3
        """
        # Proxy exceptions don't have error codes.  We want to always return
        # those unchanged as errors
        if e.code is None:
            return e

        # RoutingExceptions are used internally to trigger routing
        # actions, such as slash redirects raising RequestRedirect. They
        # are not raised or handled in user code.
        if isinstance(e, RoutingException):
            return e

        handler = self._find_error_handler(e)
        if handler is None:
            return e
        return self.ensure_sync(handler)(e)

    def trap_http_exception(self, e: Exception) -> bool:
        """Checks if an HTTP exception should be trapped or not.  By default
        this will return ``False`` for all exceptions except for a bad request
        key error if ``TRAP_BAD_REQUEST_ERRORS`` is set to ``True``.  It
        also returns ``True`` if ``TRAP_HTTP_EXCEPTIONS`` is set to ``True``.

        This is called for all HTTP exceptions raised by a view function.
        If it returns ``True`` for any exception the error handler for this
        exception is not called and it shows up as regular exception in the
        traceback.  This is helpful for debugging implicitly raised HTTP
        exceptions.

        .. versionchanged:: 1.0
            Bad request errors are not trapped by default in debug mode.

        .. versionadded:: 0.8
        """
        if self.config["TRAP_HTTP_EXCEPTIONS"]:
            return True

        trap_bad_request = self.config["TRAP_BAD_REQUEST_ERRORS"]

        # if unset, trap key errors in debug mode
        if (
                trap_bad_request is None
                and self.debug
                and isinstance(e, BadRequestKeyError)
        ):
            return True

        if trap_bad_request:
            return isinstance(e, BadRequest)

        return False

    def handle_user_exception(
            self, e: Exception
    ) -> t.Union[HTTPException, ResponseReturnValue]:
        """This method is called whenever an exception occurs that
        should be handled. A special case is :class:`~werkzeug
        .exceptions.HTTPException` which is forwarded to the
        :meth:`handle_http_exception` method. This function will either
        return a response value or reraise the exception with the same
        traceback.

        .. versionchanged:: 1.0
            Key errors raised from request data like ``form`` show the
            bad key in debug mode rather than a generic bad request
            message.

        .. versionadded:: 0.7
        """
        if isinstance(e, BadRequestKeyError) and (
                self.debug or self.config["TRAP_BAD_REQUEST_ERRORS"]
        ):
            e.show_exception = True

        if isinstance(e, HTTPException) and not self.trap_http_exception(e):
            return self.handle_http_exception(e)

        handler = self._find_error_handler(e)

        if handler is None:
            raise

        return self.ensure_sync(handler)(e)

    def handle_exception(self, e: Exception) -> Response:
        """Handle an exception that did not have an error handler
        associated with it, or that was raised from an error handler.
        This always causes a 500 ``InternalServerError``.

        Always sends the :data:`got_request_exception` signal.

        If :attr:`propagate_exceptions` is ``True``, such as in debug
        mode, the error will be re-raised so that the debugger can
        display it. Otherwise, the original exception is logged, and
        an :exc:`~werkzeug.exceptions.InternalServerError` is returned.

        If an error handler is registered for ``InternalServerError`` or
        ``500``, it will be used. For consistency, the handler will
        always receive the ``InternalServerError``. The original
        unhandled exception is available as ``e.original_exception``.

        .. versionchanged:: 1.1.0
            Always passes the ``InternalServerError`` instance to the
            handler, setting ``original_exception`` to the unhandled
            error.

        .. versionchanged:: 1.1.0
            ``after_request`` functions and other finalization is done
            even for the default 500 response when there is no handler.

        .. versionadded:: 0.3
        """
        exc_info = sys.exc_info()
        got_request_exception.send(self, exception=e)

        if self.propagate_exceptions:
            # Re-raise if called with an active exception, otherwise
            # raise the passed in exception.
            if exc_info[1] is e:
                raise

            raise e

        self.log_exception(exc_info)
        server_error: t.Union[InternalServerError, ResponseReturnValue]
        server_error = InternalServerError(original_exception=e)
        handler = self._find_error_handler(server_error)

        if handler is not None:
            server_error = self.ensure_sync(handler)(server_error)

        return self.finalize_request(server_error, from_error_handler=True)

    def log_exception(
            self,
            exc_info: t.Union[
                t.Tuple[type, BaseException, TracebackType], t.Tuple[None, None, None]
            ],
    ) -> None:
        """Logs an exception.  This is called by :meth:`handle_exception`
        if debugging is disabled and right before the handler is called.
        The default implementation logs the exception as error on the
        :attr:`logger`.

        .. versionadded:: 0.8
        """
        self.logger.error(
            f"Exception on {request.path} [{request.method}]", exc_info=exc_info
        )

    def raise_routing_exception(self, request: Request) -> "te.NoReturn":
        """Exceptions that are recording during routing are reraised with
        this method.  During debug we are not reraising redirect requests
        for non ``GET``, ``HEAD``, or ``OPTIONS`` requests and we're raising
        a different error instead to help debug situations.

        :internal:
        """
        if (
                not self.debug
                or not isinstance(request.routing_exception, RequestRedirect)
                or request.method in ("GET", "HEAD", "OPTIONS")
        ):
            raise request.routing_exception  # type: ignore

        from .debughelpers import FormDataRoutingRedirect

        raise FormDataRoutingRedirect(request)

    def dispatch_request(self) -> ResponseReturnValue:
        """请求的分发工作，根据 URL 规则匹配找到对应的视图函数，并将请求参数传递给视图函数执行处理。
        """
        req = _request_ctx_stack.top.request
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
        rule = req.url_rule
        # 根据规则决定是否提供自动响应选项，
        # 如果请求使用 OPTIONS 方法，并且为该 URL 提供自动响应选项，则返回默认的 OPTIONS 响应
        if (
                getattr(rule, "provide_automatic_options", False)
                and req.method == "OPTIONS"
        ):
            return self.make_default_options_response()
        # otherwise dispatch to the handler for that endpoint
        return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)

    def full_dispatch_request(self) -> Response:
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.

        .. versionadded:: 0.7
        """
        self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
        return self.finalize_request(rv)

    def finalize_request(
            self,
            rv: t.Union[ResponseReturnValue, HTTPException],
            from_error_handler: bool = False,
    ) -> Response:
        """
        用于将视图函数的返回值或 HTTP 异常转换为响应对象，并进行最终的处理。
        这包括对响应对象的附加处理操作，发送请求完成的信号，并处理异常情况
        """
        response = self.make_response(rv)
        try:
            response = self.process_response(response)
            request_finished.send(self, response=response)
        except Exception:
            if not from_error_handler:
                raise
            self.logger.exception(
                "Request finalizing failed with an error while handling an error"
            )
        return response

    def try_trigger_before_first_request_functions(self) -> None:
        """Called before each request and will ensure that it triggers
        the :attr:`before_first_request_funcs` and only exactly once per
        application instance (which means process usually).

        :internal:
        """
        if self._got_first_request:
            return
        with self._before_request_lock:
            if self._got_first_request:
                return
            for func in self.before_first_request_funcs:
                self.ensure_sync(func)()
            self._got_first_request = True

    def make_default_options_response(self) -> Response:
        """This method is called to create the default ``OPTIONS`` response.
        This can be changed through subclassing to change the default
        behavior of ``OPTIONS`` responses.

        .. versionadded:: 0.7
        """
        adapter = _request_ctx_stack.top.url_adapter
        methods = adapter.allowed_methods()
        rv = self.response_class()
        rv.allow.update(methods)
        return rv

    def should_ignore_error(self, error: t.Optional[BaseException]) -> bool:
        """This is called to figure out if an error should be ignored
        or not as far as the teardown system is concerned.  If this
        function returns ``True`` then the teardown handlers will not be
        passed the error.

        .. versionadded:: 0.10
        """
        return False

    def ensure_sync(self, func: t.Callable) -> t.Callable:
        """
        如果 func 是普通的同步函数（plain def 函数），则直接返回该函数本身，不做任何修改。
        如果 func 是异步函数（async def 函数），则通过 async_to_sync 方法将其包装，以便在运行和等待响应时适应异步函数的特性。
        """
        if iscoroutinefunction(func):
            return self.async_to_sync(func)

        return func

    def async_to_sync(
            self, func: t.Callable[..., t.Coroutine]
    ) -> t.Callable[..., t.Any]:
        """Return a sync function that will run the coroutine function.

        .. code-block:: python

            result = app.async_to_sync(func)(*args, **kwargs)

        Override this method to change how the app converts async code
        to be synchronously callable.

        .. versionadded:: 2.0
        """
        try:
            from asgiref.sync import async_to_sync as asgiref_async_to_sync
        except ImportError:
            raise RuntimeError(
                "Install Flask with the 'async' extra in order to use async views."
            )

        # Check that Werkzeug isn't using its fallback ContextVar class.
        if ContextVar.__module__ == "werkzeug.local":
            raise RuntimeError(
                "Async cannot be used with this combination of Python "
                "and Greenlet versions."
            )

        return asgiref_async_to_sync(func)

    def make_response(self, rv: ResponseReturnValue) -> Response:
        """
        接受视图函数的返回值作为参数，然后根据不同类型的返回值进行相应的处理，最终将其转换为一个响应对象并返回。
        必须返回Response对象。
        可以是：
            str：将字符串编码为 UTF-8 后作为响应对象的正文内容。
            bytes：直接作为响应对象的正文内容。
            dict：将字典转换为 JSON 格式后作为响应对象的正文内容。
            tuple：可以是 (body, status, headers)、(body, status) 或 (body, headers) 的形式，分别表示响应对象的主体内容、状态码和响应头。

            :attr:`response_class`：原样返回
            :class:`~werkzeug.wrappers.Response`：强制转换为Response
            :func:`callable`：该函数被称为 WSGI 应用程序。 结果用于创建响应对象。
        """

        status = headers = None

        # 解包tuple
        if isinstance(rv, tuple):
            len_rv = len(rv)

            # 3元组直接解包
            if len_rv == 3:
                rv, status, headers = rv
            # 确定 2 元组是否有状态或标头
            elif len_rv == 2:
                if isinstance(rv[1], (Headers, dict, tuple, list)):
                    rv, headers = rv
                else:
                    rv, status = rv
            # 其它情况，抛出异常
            else:
                raise TypeError(
                    "The view function did not return a valid response tuple."
                    " The tuple must have the form (body, status, headers),"
                    " (body, status), or (body, headers)."
                )

        # body不能为空
        if rv is None:
            raise TypeError(
                f"The view function for {request.endpoint!r} did not"
                " return a valid response. The function either returned"
                " None or ended without a return statement."
            )

        # make sure the body is an instance of the response class
        if not isinstance(rv, self.response_class):
            if isinstance(rv, (str, bytes, bytearray)):
                rv = self.response_class(rv, status=status, headers=headers)
                status = headers = None
            elif isinstance(rv, dict):
                rv = jsonify(rv)
            elif isinstance(rv, BaseResponse) or callable(rv):
                # evaluate a WSGI callable, or coerce a different response
                # class to the correct type
                try:
                    rv = self.response_class.force_type(rv, request.environ)  # type: ignore  # noqa: B950
                except TypeError as e:
                    raise TypeError(
                        f"{e}\nThe view function did not return a valid"
                        " response. The return type must be a string,"
                        " dict, tuple, Response instance, or WSGI"
                        f" callable, but it was a {type(rv).__name__}."
                    ).with_traceback(sys.exc_info()[2])
            else:
                raise TypeError(
                    "The view function did not return a valid"
                    " response. The return type must be a string,"
                    " dict, tuple, Response instance, or WSGI"
                    f" callable, but it was a {type(rv).__name__}."
                )

        rv = t.cast(Response, rv)
        # prefer the status if it was provided
        if status is not None:
            if isinstance(status, (str, bytes, bytearray)):
                rv.status = status  # type: ignore
            else:
                rv.status_code = status

        # extend existing headers with provided headers
        if headers:
            rv.headers.update(headers)

        return rv

    def create_url_adapter(
            self, request: t.Optional[Request]
    ) -> t.Optional[MapAdapter]:
        """
        用于创建 URL 适配器（URL Adapter）的方法。URL 适配器用于处理请求的 URL 规则和视图函数之间的关系。
        """
        if request is not None:
            # If subdomain matching is disabled (the default), use the
            # default subdomain in all cases. This should be the default
            # in Werkzeug but it currently does not have that feature.
            if not self.subdomain_matching:
                subdomain = self.url_map.default_subdomain or None
            else:
                subdomain = None

            return self.url_map.bind_to_environ(
                request.environ,
                server_name=self.config["SERVER_NAME"],
                subdomain=subdomain,
            )
        # We need at the very least the server name to be set for this
        # to work.
        if self.config["SERVER_NAME"] is not None:
            return self.url_map.bind(
                self.config["SERVER_NAME"],
                script_name=self.config["APPLICATION_ROOT"],
                url_scheme=self.config["PREFERRED_URL_SCHEME"],
            )

        return None

    def inject_url_defaults(self, endpoint: str, values: dict) -> None:
        """Injects the URL defaults for the given endpoint directly into
        the values dictionary passed.  This is used internally and
        automatically called on URL building.

        .. versionadded:: 0.7
        """
        funcs: t.Iterable[URLDefaultCallable] = self.url_default_functions[None]

        if "." in endpoint:
            # This is called by url_for, which can be called outside a
            # request, can't use request.blueprints.
            bps = _split_blueprint_path(endpoint.rpartition(".")[0])
            bp_funcs = chain.from_iterable(self.url_default_functions[bp] for bp in bps)
            funcs = chain(funcs, bp_funcs)

        for func in funcs:
            func(endpoint, values)

    def handle_url_build_error(
            self, error: Exception, endpoint: str, values: dict
    ) -> str:
        """Handle :class:`~werkzeug.routing.BuildError` on
        :meth:`url_for`.
        """
        for handler in self.url_build_error_handlers:
            try:
                rv = handler(error, endpoint, values)
            except BuildError as e:
                # make error available outside except block
                error = e
            else:
                if rv is not None:
                    return rv

        # Re-raise if called with an active exception, otherwise raise
        # the passed in exception.
        if error is sys.exc_info()[1]:
            raise

        raise error

    def preprocess_request(self) -> t.Optional[ResponseReturnValue]:
        """在发送请求之前调用。 调用在应用程序和当前蓝图（如果有）中注册的 url_value_preprocessors。
        然后调用在应用程序和蓝图上注册的 before_request_funcs 。

         如果任何 before_request 处理程序返回非 None 值，则该值将被视为视图的返回值，并停止进一步的请求处理。
        """

        funcs: t.Iterable[URLValuePreprocessorCallable] = self.url_value_preprocessors[
            None
        ]
        for bp in request.blueprints:
            if bp in self.url_value_preprocessors:
                funcs = chain(funcs, self.url_value_preprocessors[bp])
        for func in funcs:
            func(request.endpoint, request.view_args)

        funcs: t.Iterable[BeforeRequestCallable] = self.before_request_funcs[None]
        for bp in request.blueprints:
            if bp in self.before_request_funcs:
                funcs = chain(funcs, self.before_request_funcs[bp])
        for func in funcs:
            rv = self.ensure_sync(func)()
            if rv is not None:
                return rv

        return None

    def process_response(self, response: Response) -> Response:
        """
        调用所有的_after_request_functions
        """
        ctx = _request_ctx_stack.top
        funcs: t.Iterable[AfterRequestCallable] = ctx._after_request_functions
        for bp in request.blueprints:
            if bp in self.after_request_funcs:
                funcs = chain(funcs, reversed(self.after_request_funcs[bp]))
        if None in self.after_request_funcs:
            funcs = chain(funcs, reversed(self.after_request_funcs[None]))
        for handler in funcs:
            response = self.ensure_sync(handler)(response)
        if not self.session_interface.is_null_session(ctx.session):
            self.session_interface.save_session(self, ctx.session, response)
        return response

    def do_teardown_request(
            self, exc: t.Optional[BaseException] = _sentinel  # type: ignore
    ) -> None:
        """
        在分发请求并返回响应之后、弹出请求上下文之前调用。
        """
        if exc is _sentinel:
            exc = sys.exc_info()[1]
        funcs: t.Iterable[TeardownCallable] = reversed(
            self.teardown_request_funcs[None]
        )
        for bp in request.blueprints:
            if bp in self.teardown_request_funcs:
                funcs = chain(funcs, reversed(self.teardown_request_funcs[bp]))
        for func in funcs:
            self.ensure_sync(func)(exc)
        request_tearing_down.send(self, exc=exc)

    def do_teardown_appcontext(
            self, exc: t.Optional[BaseException] = _sentinel  # type: ignore
    ) -> None:
        """Called right before the application context is popped.

        When handling a request, the application context is popped
        after the request context. See :meth:`do_teardown_request`.

        This calls all functions decorated with
        :meth:`teardown_appcontext`. Then the
        :data:`appcontext_tearing_down` signal is sent.

        This is called by
        :meth:`AppContext.pop() <flask.ctx.AppContext.pop>`.

        .. versionadded:: 0.9
        """
        if exc is _sentinel:
            exc = sys.exc_info()[1]
        for func in reversed(self.teardown_appcontext_funcs):
            self.ensure_sync(func)(exc)
        appcontext_tearing_down.send(self, exc=exc)

    def app_context(self) -> AppContext:
        """创建一个:class:`~flask.ctx.AppContext`。 用作“with”块来推送上下文，这将使 current_app 指向此应用程序。

         在处理请求和运行 CLI 命令时，RequestContext.push() <flask.ctx.RequestContext.push>` 自动推送应用程序上下文。 使用它可以在这些情况之外手动创建上下文。
        """
        return AppContext(self)

    def request_context(self, environ: dict) -> RequestContext:
        """
        :param environ: wsgi环境
        """
        return RequestContext(self, environ)

    def test_request_context(self, *args: t.Any, **kwargs: t.Any) -> RequestContext:
        """Create a :class:`~flask.ctx.RequestContext` for a WSGI
        environment created from the given values. This is mostly useful
        during testing, where you may want to run a function that uses
        request data without dispatching a full request.

        See :doc:`/reqcontext`.

        Use a ``with`` block to push the context, which will make
        :data:`request` point at the request for the created
        environment. ::

            with test_request_context(...):
                generate_report()

        When using the shell, it may be easier to push and pop the
        context manually to avoid indentation. ::

            ctx = app.test_request_context(...)
            ctx.push()
            ...
            ctx.pop()

        Takes the same arguments as Werkzeug's
        :class:`~werkzeug.test.EnvironBuilder`, with some defaults from
        the application. See the linked Werkzeug docs for most of the
        available arguments. Flask-specific behavior is listed here.

        :param path: URL path being requested.
        :param base_url: Base URL where the app is being served, which
            ``path`` is relative to. If not given, built from
            :data:`PREFERRED_URL_SCHEME`, ``subdomain``,
            :data:`SERVER_NAME`, and :data:`APPLICATION_ROOT`.
        :param subdomain: Subdomain name to append to
            :data:`SERVER_NAME`.
        :param url_scheme: Scheme to use instead of
            :data:`PREFERRED_URL_SCHEME`.
        :param data: The request body, either as a string or a dict of
            form keys and values.
        :param json: If given, this is serialized as JSON and passed as
            ``data``. Also defaults ``content_type`` to
            ``application/json``.
        :param args: other positional arguments passed to
            :class:`~werkzeug.test.EnvironBuilder`.
        :param kwargs: other keyword arguments passed to
            :class:`~werkzeug.test.EnvironBuilder`.
        """
        from .testing import EnvironBuilder

        builder = EnvironBuilder(self, *args, **kwargs)

        try:
            return self.request_context(builder.get_environ())
        finally:
            builder.close()

    def wsgi_app(self, environ: dict, start_response: t.Callable) -> t.Any:
        """The actual WSGI application. This is not implemented in
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        :param environ:  一个WSGI环境。
        :param start_response: 一个可调用对象，接受一个状态码、一个头部列表和一个可选的异常上下文来开始响应。
        """
        ctx = self.request_context(environ)
        error: t.Optional[BaseException] = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)

    def __call__(self, environ: dict, start_response: t.Callable) -> t.Any:
        """
        WSGI 服务器调用 Flask 应用对象作为 WSGI 应用。 这调用 :meth:`wsgi_app`，它可以被包装以应用中间件。
        """
        return self.wsgi_app(environ, start_response)
