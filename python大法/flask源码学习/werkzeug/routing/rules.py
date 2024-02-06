import ast
import re
import typing as t
from dataclasses import dataclass
from string import Template
from types import CodeType

from .._internal import _to_bytes
from ..urls import url_encode
from ..urls import url_quote
from .converters import ValidationError

if t.TYPE_CHECKING:
    from .converters import BaseConverter
    from .map import Map


class Weighting(t.NamedTuple):
    number_static_weights: int
    static_weights: t.List[t.Tuple[int, int]]
    number_argument_weights: int
    argument_weights: t.List[int]


@dataclass
class RulePart:
    """A part of a rule.

    Rules can be represented by parts as delimited by `/` with
    instances of this class representing those parts. The *content* is
    either the raw content if *static* or a regex string to match
    against. The *weight* can be used to order parts when matching.

    """

    content: str
    final: bool
    static: bool
    suffixed: bool
    weight: Weighting


_part_re = re.compile(
    r"""
    (?:
        (?P<slash>\/)                                 # a slash
      |
        (?P<static>[^<\/]+)                           # static rule data
      |
        (?:
          <
            (?:
              (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
              (?:\((?P<arguments>.*?)\))?             # converter arguments
              \:                                      # variable delimiter
            )?
            (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)      # variable name
           >
        )
    )
    """,
    re.VERBOSE,
)

_simple_rule_re = re.compile(r"<([^>]+)>")
_converter_args_re = re.compile(
    r"""
    ((?P<name>\w+)\s*=\s*)?
    (?P<value>
        True|False|
        \d+.\d+|
        \d+.|
        \d+|
        [\w\d_.]+|
        [urUR]?(?P<stringval>"[^"]*?"|'[^']*')
    )\s*,
    """,
    re.VERBOSE,
)

_PYTHON_CONSTANTS = {"None": None, "True": True, "False": False}


def _find(value: str, target: str, pos: int) -> int:
    """Find the *target* in *value* after *pos*.

    Returns the *value* length if *target* isn't found.
    """
    try:
        return value.index(target, pos)
    except ValueError:
        return len(value)


def _pythonize(value: str) -> t.Union[None, bool, int, float, str]:
    if value in _PYTHON_CONSTANTS:
        return _PYTHON_CONSTANTS[value]
    for convert in int, float:
        try:
            return convert(value)  # type: ignore
        except ValueError:
            pass
    if value[:1] == value[-1:] and value[0] in "\"'":
        value = value[1:-1]
    return str(value)


def parse_converter_args(argstr: str) -> t.Tuple[t.Tuple, t.Dict[str, t.Any]]:
    argstr += ","
    args = []
    kwargs = {}

    for item in _converter_args_re.finditer(argstr):
        value = item.group("stringval")
        if value is None:
            value = item.group("value")
        value = _pythonize(value)
        if not item.group("name"):
            args.append(value)
        else:
            name = item.group("name")
            kwargs[name] = value

    return tuple(args), kwargs


class RuleFactory:
    """As soon as you have more complex URL setups it's a good idea to use rule
    factories to avoid repetitive tasks.  Some of them are builtin, others can
    be added by subclassing `RuleFactory` and overriding `get_rules`.
    """

    def get_rules(self, map: "Map") -> t.Iterable["Rule"]:
        """Subclasses of `RuleFactory` have to override this method and return
        an iterable of rules."""
        raise NotImplementedError()


class Subdomain(RuleFactory):
    """All URLs provided by this factory have the subdomain set to a
    specific domain. For example if you want to use the subdomain for
    the current language this can be a good setup::

        url_map = Map([
            Rule('/', endpoint='#select_language'),
            Subdomain('<string(length=2):lang_code>', [
                Rule('/', endpoint='index'),
                Rule('/about', endpoint='about'),
                Rule('/help', endpoint='help')
            ])
        ])

    All the rules except for the ``'#select_language'`` endpoint will now
    listen on a two letter long subdomain that holds the language code
    for the current request.
    """

    def __init__(self, subdomain: str, rules: t.Iterable[RuleFactory]) -> None:
        self.subdomain = subdomain
        self.rules = rules

    def get_rules(self, map: "Map") -> t.Iterator["Rule"]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.subdomain = self.subdomain
                yield rule


class Submount(RuleFactory):
    """Like `Subdomain` but prefixes the URL rule with a given string::

        url_map = Map([
            Rule('/', endpoint='index'),
            Submount('/blog', [
                Rule('/', endpoint='blog/index'),
                Rule('/entry/<entry_slug>', endpoint='blog/show')
            ])
        ])

    Now the rule ``'blog/show'`` matches ``/blog/entry/<entry_slug>``.
    """

    def __init__(self, path: str, rules: t.Iterable[RuleFactory]) -> None:
        self.path = path.rstrip("/")
        self.rules = rules

    def get_rules(self, map: "Map") -> t.Iterator["Rule"]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.rule = self.path + rule.rule
                yield rule


class EndpointPrefix(RuleFactory):
    """Prefixes all endpoints (which must be strings for this factory) with
    another string. This can be useful for sub applications::

        url_map = Map([
            Rule('/', endpoint='index'),
            EndpointPrefix('blog/', [Submount('/blog', [
                Rule('/', endpoint='index'),
                Rule('/entry/<entry_slug>', endpoint='show')
            ])])
        ])
    """

    def __init__(self, prefix: str, rules: t.Iterable[RuleFactory]) -> None:
        self.prefix = prefix
        self.rules = rules

    def get_rules(self, map: "Map") -> t.Iterator["Rule"]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                rule = rule.empty()
                rule.endpoint = self.prefix + rule.endpoint
                yield rule


class RuleTemplate:
    """Returns copies of the rules wrapped and expands string templates in
    the endpoint, rule, defaults or subdomain sections.

    Here a small example for such a rule template::

        from werkzeug.routing import Map, Rule, RuleTemplate

        resource = RuleTemplate([
            Rule('/$name/', endpoint='$name.list'),
            Rule('/$name/<int:id>', endpoint='$name.show')
        ])

        url_map = Map([resource(name='user'), resource(name='page')])

    When a rule template is called the keyword arguments are used to
    replace the placeholders in all the string parameters.
    """

    def __init__(self, rules: t.Iterable["Rule"]) -> None:
        self.rules = list(rules)

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> "RuleTemplateFactory":
        return RuleTemplateFactory(self.rules, dict(*args, **kwargs))


class RuleTemplateFactory(RuleFactory):
    """A factory that fills in template variables into rules.  Used by
    `RuleTemplate` internally.

    :internal:
    """

    def __init__(
            self, rules: t.Iterable[RuleFactory], context: t.Dict[str, t.Any]
    ) -> None:
        self.rules = rules
        self.context = context

    def get_rules(self, map: "Map") -> t.Iterator["Rule"]:
        for rulefactory in self.rules:
            for rule in rulefactory.get_rules(map):
                new_defaults = subdomain = None
                if rule.defaults:
                    new_defaults = {}
                    for key, value in rule.defaults.items():
                        if isinstance(value, str):
                            value = Template(value).substitute(self.context)
                        new_defaults[key] = value
                if rule.subdomain is not None:
                    subdomain = Template(rule.subdomain).substitute(self.context)
                new_endpoint = rule.endpoint
                if isinstance(new_endpoint, str):
                    new_endpoint = Template(new_endpoint).substitute(self.context)
                yield Rule(
                    Template(rule.rule).substitute(self.context),
                    new_defaults,
                    subdomain,
                    rule.methods,
                    rule.build_only,
                    new_endpoint,
                    rule.strict_slashes,
                )


def _prefix_names(src: str) -> ast.stmt:
    """ast parse and prefix names with `.` to avoid collision with user vars"""
    tree = ast.parse(src).body[0]
    if isinstance(tree, ast.Expr):
        tree = tree.value  # type: ignore
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = f".{node.id}"
    return tree


_CALL_CONVERTER_CODE_FMT = "self._converters[{elem!r}].to_url()"
_IF_KWARGS_URL_ENCODE_CODE = """\
if kwargs:
    params = self._encode_query_vars(kwargs)
    q = "?" if params else ""
else:
    q = params = ""
"""
_IF_KWARGS_URL_ENCODE_AST = _prefix_names(_IF_KWARGS_URL_ENCODE_CODE)
_URL_ENCODE_AST_NAMES = (_prefix_names("q"), _prefix_names("params"))


class Rule(RuleFactory):
    """
    `string`:格式为<converter(arguments):name>，其中转换器和参数都是可选的。如果没有定义转换器，则使用default转换器，它表示在正常配置中使用string。
    `endpoint`: 一个与路由规则相关联的标识符，用于在应用程序中引用和生成URL。
               它可以是任何东西，如函数的引用、字符串、数字等。然而，使用字符串作为端点是首选的方式，因为端点通常用于URL生成。
    `defaults`
            url_map = Map([
                Rule('/all/', defaults={'page': 1}, endpoint='all_entries'),
                Rule('/all/page/<int:page>', endpoint='all_entries')
            ])
            当生成URL时，如果与同一端点相关的其他规则没有提供相应的值，那么将使用 defaults 字典中指定的默认值。换句话说，这个参数可以为一组相关的规则设置默认的URL参数值。

            举个例子，假设应用程序有两个路由规则，都使用了相同的端点 'all_entries'：
            /all/，不包含页码参数，默认为第一页。
            /all/page/<int:page>，包含页码参数。
            通过在第一个规则中使用 defaults={'page': 1}，你为与端点 'all_entries' 相关的其他规则设置了默认值。
            这样，如果用户访问 http://example.com/all/page/1，会被重定向到 http://example.com/all/。

    `subdomain`
        当请求的子域名与规则字符串匹配时，才会启用这条路由规则。换句话说，这个参数可以限定该路由规则只匹配特定的子域名。
        处理用户个人主页，并且每个用户可以使用自己的子域名访问其个人主页，
        比如 http://username.example.com/。可以使用 subdomain='<username>' 参数来将这个路由规则应用于具体的子域名。
            url_map = Map([
                Rule('/', subdomain='<username>', endpoint='user/homepage'),
                Rule('/stats', subdomain='<username>', endpoint='user/stats')
            ])

    `methods` 允许的http方法
    `strict_slashes` 严格斜杠，末尾斜杠是否匹配
    `merge_slashes` 合并斜杠 // -> /
    `build_only`
        将其设置为 True，规则将永远不会匹配，但会创建一个可以构建的 URL。 如果子域或文件夹上有 WSGI 应用程序未处理的资源（如静态数据），这非常有用
    `redirect_to`
        在Rule中的redirect_to参数可以是字符串或可调用对象（callable）。
        如果是可调用对象，则会使用匹配到的URL适配器和URL的值作为关键字参数调用它，并且它必须返回重定向的目标。
        如果是字符串，则必须使用规则语法中的占位符。
        如果redirect_to是可调用对象（callable），则它将使用URL适配器和URL的值作为关键字参数调用。在这个可调用对象中，您可以根据需要使用URL值来生成重定向的目标
        rule syntax::

            def foo_with_slug(adapter, id):
                return f'foo/{Foo.get_slug_for_id(id)}'

            url_map = Map([
                Rule('/foo/<slug>', endpoint='foo'),
                Rule('/some/old/url/<slug>', redirect_to='foo/<slug>'),
                Rule('/other/old/url/<int:id>', redirect_to=foo_with_slug)
            ])

        当匹配到这个规则时，路由系统会引发一个RequestRedirect异常，其中包含重定向的目标。
        需要注意的是，目标URL将与根路由进行拼接，因此除非您真的是要指向该域的根路径，否则不要在目标URL中使用前导斜杠。

    `alias`：如果启用，此规则将充当具有相同端点和参数的另一个规则的别名。
    `host`：如果提供并且 URL 映射启用了主机匹配，则可以使用它为整个主机提供匹配规则。 这也意味着子域功能被禁用。
    websocket： 如果为True，则此规则仅匹配 WebSocket（“ws://”、“wss://”）请求。
    """

    def __init__(
            self,
            string: str,
            defaults: t.Optional[t.Mapping[str, t.Any]] = None,
            subdomain: t.Optional[str] = None,
            methods: t.Optional[t.Iterable[str]] = None,
            build_only: bool = False,
            endpoint: t.Optional[str] = None,
            strict_slashes: t.Optional[bool] = None,
            merge_slashes: t.Optional[bool] = None,
            redirect_to: t.Optional[t.Union[str, t.Callable[..., str]]] = None,
            alias: bool = False,
            host: t.Optional[str] = None,
            websocket: bool = False,
    ) -> None:
        if not string.startswith("/"):
            raise ValueError("urls must start with a leading slash")
        self.rule = string
        self.is_leaf = not string.endswith("/")
        self.is_branch = string.endswith("/")

        self.map: "Map" = None  # type: ignore
        self.strict_slashes = strict_slashes
        self.merge_slashes = merge_slashes
        self.subdomain = subdomain
        self.host = host
        self.defaults = defaults
        self.build_only = build_only
        self.alias = alias
        self.websocket = websocket

        if methods is not None:
            if isinstance(methods, str):
                raise TypeError("'methods' should be a list of strings.")

            methods = {x.upper() for x in methods}

            if "HEAD" not in methods and "GET" in methods:
                methods.add("HEAD")

            if websocket and methods - {"GET", "HEAD", "OPTIONS"}:
                raise ValueError(
                    "WebSocket rules can only use 'GET', 'HEAD', and 'OPTIONS' methods."
                )

        self.methods = methods
        self.endpoint: str = endpoint  # type: ignore
        self.redirect_to = redirect_to

        if defaults:
            self.arguments = set(map(str, defaults))
        else:
            self.arguments = set()

        self._converters: t.Dict[str, "BaseConverter"] = {}
        self._trace: t.List[t.Tuple[bool, str]] = []
        self._parts: t.List[RulePart] = []

    def empty(self) -> "Rule":
        """
        Return an unbound copy of this rule.

        This can be useful if want to reuse an already bound URL for another
        map.  See ``get_empty_kwargs`` to override what keyword arguments are
        provided to the new copy.
        """
        return type(self)(self.rule, **self.get_empty_kwargs())

    def get_empty_kwargs(self) -> t.Mapping[str, t.Any]:
        """
        Provides kwargs for instantiating empty copy with empty()

        Use this method to provide custom keyword arguments to the subclass of
        ``Rule`` when calling ``some_rule.empty()``.  Helpful when the subclass
        has custom keyword arguments that are needed at instantiation.

        Must return a ``dict`` that will be provided as kwargs to the new
        instance of ``Rule``, following the initial ``self.rule`` value which
        is always provided as the first, required positional argument.
        """
        defaults = None
        if self.defaults:
            defaults = dict(self.defaults)
        return dict(
            defaults=defaults,
            subdomain=self.subdomain,
            methods=self.methods,
            build_only=self.build_only,
            endpoint=self.endpoint,
            strict_slashes=self.strict_slashes,
            redirect_to=self.redirect_to,
            alias=self.alias,
            host=self.host,
        )

    def get_rules(self, map: "Map") -> t.Iterator["Rule"]:
        yield self

    def refresh(self) -> None:
        """Rebinds and refreshes the URL.  Call this if you modified the
        rule in place.

        :internal:
        """
        self.bind(self.map, rebind=True)

    def bind(self, map: "Map", rebind: bool = False) -> None:
        """Bind the url to a map and create a regular expression based on
        the information from the rule itself and the defaults from the map.

        :internal:
        """
        if self.map is not None and not rebind:
            raise RuntimeError(f"url rule {self!r} already bound to map {self.map!r}")
        self.map = map
        if self.strict_slashes is None:
            self.strict_slashes = map.strict_slashes
        if self.merge_slashes is None:
            self.merge_slashes = map.merge_slashes
        if self.subdomain is None:
            self.subdomain = map.default_subdomain
        self.compile()

    def get_converter(
            self,
            variable_name: str,
            converter_name: str,
            args: t.Tuple,
            kwargs: t.Mapping[str, t.Any],
    ) -> "BaseConverter":
        """Looks up the converter for the given parameter.

        .. versionadded:: 0.9
        """
        if converter_name not in self.map.converters:
            raise LookupError(f"the converter {converter_name!r} does not exist")
        return self.map.converters[converter_name](self.map, *args, **kwargs)

    def _encode_query_vars(self, query_vars: t.Mapping[str, t.Any]) -> str:
        return url_encode(
            query_vars,
            charset=self.map.charset,
            sort=self.map.sort_parameters,
            key=self.map.sort_key,
        )

    def _parse_rule(self, rule: str) -> t.Iterable[RulePart]:
        content = ""
        static = True
        argument_weights = []
        static_weights: t.List[t.Tuple[int, int]] = []
        final = False

        pos = 0
        while pos < len(rule):
            match = _part_re.match(rule, pos)
            if match is None:
                raise ValueError(f"malformed url rule: {rule!r}")

            data = match.groupdict()
            if data["static"] is not None:
                static_weights.append((len(static_weights), -len(data["static"])))
                self._trace.append((False, data["static"]))
                content += data["static"] if static else re.escape(data["static"])

            if data["variable"] is not None:
                if static:
                    # Switching content to represent regex, hence the need to escape
                    content = re.escape(content)
                static = False
                c_args, c_kwargs = parse_converter_args(data["arguments"] or "")
                convobj = self.get_converter(
                    data["variable"], data["converter"] or "default", c_args, c_kwargs
                )
                self._converters[data["variable"]] = convobj
                self.arguments.add(data["variable"])
                if not convobj.part_isolating:
                    final = True
                content += f"({convobj.regex})"
                argument_weights.append(convobj.weight)
                self._trace.append((True, data["variable"]))

            if data["slash"] is not None:
                self._trace.append((False, "/"))
                if final:
                    content += "/"
                else:
                    if not static:
                        content += r"\Z"
                    weight = Weighting(
                        -len(static_weights),
                        static_weights,
                        -len(argument_weights),
                        argument_weights,
                    )
                    yield RulePart(
                        content=content,
                        final=final,
                        static=static,
                        suffixed=False,
                        weight=weight,
                    )
                    content = ""
                    static = True
                    argument_weights = []
                    static_weights = []
                    final = False

            pos = match.end()

        suffixed = False
        if final and content[-1] == "/":
            # If a converter is part_isolating=False (matches slashes) and ends with a
            # slash, augment the regex to support slash redirects.
            suffixed = True
            content = content[:-1] + "(?<!/)(/?)"
        if not static:
            content += r"\Z"
        weight = Weighting(
            -len(static_weights),
            static_weights,
            -len(argument_weights),
            argument_weights,
        )
        yield RulePart(
            content=content,
            final=final,
            static=static,
            suffixed=suffixed,
            weight=weight,
        )
        if suffixed:
            yield RulePart(
                content="", final=False, static=True, suffixed=False, weight=weight
            )

    def compile(self) -> None:
        """Compiles the regular expression and stores it."""
        assert self.map is not None, "rule not bound"

        if self.map.host_matching:
            domain_rule = self.host or ""
        else:
            domain_rule = self.subdomain or ""
        self._parts = []
        self._trace = []
        self._converters = {}
        if domain_rule == "":
            self._parts = [
                RulePart(
                    content="",
                    final=False,
                    static=True,
                    suffixed=False,
                    weight=Weighting(0, [], 0, []),
                )
            ]
        else:
            self._parts.extend(self._parse_rule(domain_rule))
        self._trace.append((False, "|"))
        rule = self.rule
        if self.merge_slashes:
            rule = re.sub("/{2,}?", "/", self.rule)
        self._parts.extend(self._parse_rule(rule))

        self._build: t.Callable[..., t.Tuple[str, str]]
        self._build = self._compile_builder(False).__get__(self, None)
        self._build_unknown: t.Callable[..., t.Tuple[str, str]]
        self._build_unknown = self._compile_builder(True).__get__(self, None)

    @staticmethod
    def _get_func_code(code: CodeType, name: str) -> t.Callable[..., t.Tuple[str, str]]:
        globs: t.Dict[str, t.Any] = {}
        locs: t.Dict[str, t.Any] = {}
        exec(code, globs, locs)
        return locs[name]  # type: ignore

    def _compile_builder(
            self, append_unknown: bool = True
    ) -> t.Callable[..., t.Tuple[str, str]]:
        defaults = self.defaults or {}
        dom_ops: t.List[t.Tuple[bool, str]] = []
        url_ops: t.List[t.Tuple[bool, str]] = []

        opl = dom_ops
        for is_dynamic, data in self._trace:
            if data == "|" and opl is dom_ops:
                opl = url_ops
                continue
            # this seems like a silly case to ever come up but:
            # if a default is given for a value that appears in the rule,
            # resolve it to a constant ahead of time
            if is_dynamic and data in defaults:
                data = self._converters[data].to_url(defaults[data])
                opl.append((False, data))
            elif not is_dynamic:
                opl.append(
                    (False, url_quote(_to_bytes(data, self.map.charset), safe="/:|+"))
                )
            else:
                opl.append((True, data))

        def _convert(elem: str) -> ast.stmt:
            ret = _prefix_names(_CALL_CONVERTER_CODE_FMT.format(elem=elem))
            ret.args = [ast.Name(str(elem), ast.Load())]  # type: ignore  # str for py2
            return ret

        def _parts(ops: t.List[t.Tuple[bool, str]]) -> t.List[ast.AST]:
            parts = [
                _convert(elem) if is_dynamic else ast.Str(s=elem)
                for is_dynamic, elem in ops
            ]
            parts = parts or [ast.Str("")]
            # constant fold
            ret = [parts[0]]
            for p in parts[1:]:
                if isinstance(p, ast.Str) and isinstance(ret[-1], ast.Str):
                    ret[-1] = ast.Str(ret[-1].s + p.s)
                else:
                    ret.append(p)
            return ret

        dom_parts = _parts(dom_ops)
        url_parts = _parts(url_ops)
        if not append_unknown:
            body = []
        else:
            body = [_IF_KWARGS_URL_ENCODE_AST]
            url_parts.extend(_URL_ENCODE_AST_NAMES)

        def _join(parts: t.List[ast.AST]) -> ast.AST:
            if len(parts) == 1:  # shortcut
                return parts[0]
            return ast.JoinedStr(parts)

        body.append(
            ast.Return(ast.Tuple([_join(dom_parts), _join(url_parts)], ast.Load()))
        )

        pargs = [
            elem
            for is_dynamic, elem in dom_ops + url_ops
            if is_dynamic and elem not in defaults
        ]
        kargs = [str(k) for k in defaults]

        func_ast: ast.FunctionDef = _prefix_names("def _(): pass")  # type: ignore
        func_ast.name = f"<builder:{self.rule!r}>"
        func_ast.args.args.append(ast.arg(".self", None))
        for arg in pargs + kargs:
            func_ast.args.args.append(ast.arg(arg, None))
        func_ast.args.kwarg = ast.arg(".kwargs", None)
        for _ in kargs:
            func_ast.args.defaults.append(ast.Str(""))
        func_ast.body = body

        # use `ast.parse` instead of `ast.Module` for better portability
        # Python 3.8 changes the signature of `ast.Module`
        module = ast.parse("")
        module.body = [func_ast]

        # mark everything as on line 1, offset 0
        # less error-prone than `ast.fix_missing_locations`
        # bad line numbers cause an assert to fail in debug builds
        for node in ast.walk(module):
            if "lineno" in node._attributes:
                node.lineno = 1
            if "end_lineno" in node._attributes:
                node.end_lineno = node.lineno  # type: ignore[attr-defined]
            if "col_offset" in node._attributes:
                node.col_offset = 0
            if "end_col_offset" in node._attributes:
                node.end_col_offset = node.col_offset  # type: ignore[attr-defined]

        code = compile(module, "<werkzeug routing>", "exec")
        return self._get_func_code(code, func_ast.name)

    def build(
            self, values: t.Mapping[str, t.Any], append_unknown: bool = True
    ) -> t.Optional[t.Tuple[str, str]]:
        """Assembles the relative url for that rule and the subdomain.
        If building doesn't work for some reasons `None` is returned.

        :internal:
        """
        try:
            if append_unknown:
                return self._build_unknown(**values)
            else:
                return self._build(**values)
        except ValidationError:
            return None

    def provides_defaults_for(self, rule: "Rule") -> bool:
        """Check if this rule has defaults for a given rule.

        :internal:
        """
        return bool(
            not self.build_only
            and self.defaults
            and self.endpoint == rule.endpoint
            and self != rule
            and self.arguments == rule.arguments
        )

    def suitable_for(
            self, values: t.Mapping[str, t.Any], method: t.Optional[str] = None
    ) -> bool:
        """Check if the dict of values has enough data for url generation.

        :internal:
        """
        # if a method was given explicitly and that method is not supported
        # by this rule, this rule is not suitable.
        if (
                method is not None
                and self.methods is not None
                and method not in self.methods
        ):
            return False

        defaults = self.defaults or ()

        # all arguments required must be either in the defaults dict or
        # the value dictionary otherwise it's not suitable
        for key in self.arguments:
            if key not in defaults and key not in values:
                return False

        # in case defaults are given we ensure that either the value was
        # skipped or the value is the same as the default value.
        if defaults:
            for key, value in defaults.items():
                if key in values and value != values[key]:
                    return False

        return True

    def build_compare_key(self) -> t.Tuple[int, int, int]:
        """The build compare key for sorting.

        :internal:
        """
        return (1 if self.alias else 0, -len(self.arguments), -len(self.defaults or ()))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self._trace == other._trace

    __hash__ = None  # type: ignore

    def __str__(self) -> str:
        return self.rule

    def __repr__(self) -> str:
        if self.map is None:
            return f"<{type(self).__name__} (unbound)>"
        parts = []
        for is_dynamic, data in self._trace:
            if is_dynamic:
                parts.append(f"<{data}>")
            else:
                parts.append(data)
        parts = "".join(parts).lstrip("|")
        methods = f" ({', '.join(self.methods)})" if self.methods is not None else ""
        return f"<{type(self).__name__} {parts!r}{methods} -> {self.endpoint}>"
