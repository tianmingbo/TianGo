import copy
import math
import operator
import typing as t
from contextvars import ContextVar
from functools import partial
from functools import update_wrapper
from operator import attrgetter

from .wsgi import ClosingIterator

if t.TYPE_CHECKING:
    from _typeshed.wsgi import StartResponse
    from _typeshed.wsgi import WSGIApplication
    from _typeshed.wsgi import WSGIEnvironment

T = t.TypeVar("T")
# 创建了泛型类型变量 F，并通过 bound 参数指定了它必须是可调用类型。t.Callable[..., t.Any] 表示接受任意参数并返回任意类型的可调用对象
F = t.TypeVar("F", bound=t.Callable[..., t.Any])


def release_local(local: t.Union["Local", "LocalStack"]) -> None:
    """
    释放在 Local 或 LocalStack 中当前上下文中的数据
    """
    local.__release_local__()


class Local:
    """
    创建一个命名空间，允许存储和访问本地数据，并且能够在不同的上下文中共享这些数据.
    用于创建一个命名空间的上下文本地数据,通过包装一个 ContextVar 来存储一个 dict 类型的值.
    """

    __slots__ = ("__storage",)

    def __init__(
            self, context_var: t.Optional[ContextVar[t.Dict[str, t.Any]]] = None
    ) -> None:
        """
        初始化 Local 类的实例。它接受一个可选的 context_var 参数，这个参数是一个 ContextVar 类型的上下文变量，用于存储本地数据。
        如果没有提供 context_var，则会创建一个新的 ContextVa
        """
        if context_var is None:
            context_var = ContextVar(f"werkzeug.Local<{id(self)}>.storage")

        object.__setattr__(self, "_Local__storage", context_var)

    def __iter__(self) -> t.Iterator[t.Tuple[str, t.Any]]:
        """
        返回一个迭代器，用来迭代本地数据的键值对。
        """
        return iter(self.__storage.get({}).items())

    def __call__(
            self, name: str, *, unbound_message: t.Optional[str] = None
    ) -> "LocalProxy":
        """
        创建一个 LocalProxy 对象，用于访问本地命名空间上的属性。
        """
        return LocalProxy(self, name, unbound_message=unbound_message)

    def __release_local__(self) -> None:
        """
        清除本地数据
        """
        self.__storage.set({})

    def __getattr__(self, name: str) -> t.Any:
        values = self.__storage.get({})

        if name in values:
            return values[name]

        raise AttributeError(name)

    def __setattr__(self, name: str, value: t.Any) -> None:
        values = self.__storage.get({}).copy()
        values[name] = value
        self.__storage.set(values)

    def __delattr__(self, name: str) -> None:
        values = self.__storage.get({})

        if name in values:
            values = values.copy()
            del values[name]
            self.__storage.set(values)
        else:
            raise AttributeError(name)


class LocalStack(t.Generic[T]):
    """
    提供了一种在上下文中存储和使用栈结构的方法，允许在不同的上下文中共享和访问栈中的数据
    """

    # 限制了类实例中只能存在一个名为 _storage 的属性。这意味着类的实例只能访问和操作 _storage 属性，而不能动态地添加或修改其他属性。
    __slots__ = ("_storage",)

    def __init__(self, context_var: t.Optional[ContextVar[t.List[T]]] = None) -> None:
        """
        初始化 LocalStack 类的实例。它接受一个可选的 context_var 参数，这个参数是一个 ContextVar 实例，用于存储本地栈的数据。
        如果没有提供 context_var，则会创建一个新的 ContextVar。
        """
        if context_var is None:
            context_var = ContextVar(f"werkzeug.LocalStack<{id(self)}>.storage")

        self._storage = context_var

    def __release_local__(self) -> None:
        """
        清除本地栈中的数据。
        """
        self._storage.set([])

    def push(self, obj: T) -> t.List[T]:
        """将一个新的项添加到栈的顶部，并返回修改后的栈"""
        stack = self._storage.get([]).copy()
        stack.append(obj)
        self._storage.set(stack)
        return stack

    def pop(self) -> t.Optional[T]:
        """
        从栈的顶部移除一个项，并返回移除的项。如果栈为空，则返回 None
        """
        stack = self._storage.get([])

        if len(stack) == 0:
            return None

        rv = stack[-1]
        self._storage.set(stack[:-1])
        return rv

    @property
    def top(self) -> t.Optional[T]:
        """
        返回栈顶的项。如果栈为空，则返回 None
        """
        stack = self._storage.get([])
        if len(stack) == 0:
            return None

        return stack[-1]

    def __call__(
            self, name: t.Optional[str] = None, *, unbound_message: t.Optional[str] = None
    ) -> "LocalProxy":
        """
        创建一个 LocalProxy 对象，用于访问本地栈的顶部项
        """
        return LocalProxy(self, name, unbound_message=unbound_message)


class LocalManager:
    """
    管理当前上下文中一个或多个Local和LocalStack对象的数据释放
    """

    __slots__ = ("locals",)

    def __init__(
            self,
            locals: t.Optional[t.Union[Local, LocalStack, t.Iterable[t.Union[Local, LocalStack]]]] = None,
    ) -> None:
        if locals is None:
            self.locals = []
        elif isinstance(locals, Local):
            self.locals = [locals]
        else:
            self.locals = list(locals)  # type: ignore[arg-type]

    def cleanup(self) -> None:
        """
        释放当前上下文中的locals对象中的数据。在每个请求结束时调用该方法
        """
        for local in self.locals:
            release_local(local)

    def make_middleware(self, app: "WSGIApplication") -> "WSGIApplication":
        """
        将一个WSGI应用程序包装起来，以便在响应发送后自动释放本地数据
        """

        def application(
                environ: "WSGIEnvironment", start_response: "StartResponse"
        ) -> t.Iterable[bytes]:
            return ClosingIterator(app(environ, start_response), self.cleanup)

        return application

    def middleware(self, func: "WSGIApplication") -> "WSGIApplication":
        """
        作为一个装饰器应用在WSGI应用程序函数上
        """
        return update_wrapper(self.make_middleware(func), func)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} storages: {len(self.locals)}>"


class _ProxyLookup:
    """
    这是一个处理 :class:LocalProxy 的属性查找的描述符（Descriptor）。

    f：访问这个属性时使用的内置函数。不是直接查找特殊方法，而是在对象上重新执行函数调用。
    fallback：如果代理未绑定，返回这个函数，而不是引发 :exc:RuntimeError 异常。
    is_attr：被代理的名称是一个属性，而不是一个函数。立即调用回退函数来获取值。
    class_value: 当直接从 LocalProxy 类中访问时返回的值。用于 __doc__，因此可以构建文档。
    """

    __slots__ = ("bind_f", "fallback", "is_attr", "class_value", "name")

    def __init__(
            self,
            f: t.Optional[t.Callable] = None,
            fallback: t.Optional[t.Callable] = None,
            class_value: t.Optional[t.Any] = None,
            is_attr: bool = False,
    ) -> None:
        bind_f: t.Optional[t.Callable[["LocalProxy", t.Any], t.Callable]]

        if hasattr(f, "__get__"):
            # A Python function, can be turned into a bound method.

            def bind_f(instance: "LocalProxy", obj: t.Any) -> t.Callable:
                return f.__get__(obj, type(obj))  # type: ignore

        elif f is not None:
            # A C function, use partial to bind the first argument.

            def bind_f(instance: "LocalProxy", obj: t.Any) -> t.Callable:
                return partial(f, obj)

        else:
            # Use getattr, which will produce a bound method.
            bind_f = None

        self.bind_f = bind_f
        self.fallback = fallback
        self.class_value = class_value
        self.is_attr = is_attr

    def __set_name__(self, owner: "LocalProxy", name: str) -> None:
        self.name = name

    def __get__(self, instance: "LocalProxy", owner: t.Optional[type] = None) -> t.Any:
        if instance is None:
            if self.class_value is not None:
                return self.class_value

            return self

        try:
            obj = instance._get_current_object()
        except RuntimeError:
            if self.fallback is None:
                raise

            fallback = self.fallback.__get__(instance, owner)

            if self.is_attr:
                # __class__ and __doc__ are attributes, not methods.
                # Call the fallback to get the value.
                return fallback()

            return fallback

        if self.bind_f is not None:
            return self.bind_f(instance, obj)

        return getattr(obj, self.name)

    def __repr__(self) -> str:
        return f"proxy {self.name}"

    def __call__(self, instance: "LocalProxy", *args: t.Any, **kwargs: t.Any) -> t.Any:
        """
        支持从类中调用未绑定的方法。
        例如，当使用 ``copy.copy`` 时，它执行了 ``type(x).__copy__(x)``。
        由于无法代理 ``type(x)``，因此返回代理类型和描述符。
        """
        return self.__get__(instance, type(instance))(*args, **kwargs)


class _ProxyIOp(_ProxyLookup):
    """Look up an augmented assignment method on a proxied object. The
    method is wrapped to return the proxy instead of the object.
    """

    __slots__ = ()

    def __init__(
            self, f: t.Optional[t.Callable] = None, fallback: t.Optional[t.Callable] = None
    ) -> None:
        super().__init__(f, fallback)

        def bind_f(instance: "LocalProxy", obj: t.Any) -> t.Callable:
            def i_op(self: t.Any, other: t.Any) -> "LocalProxy":
                f(self, other)  # type: ignore
                return instance

            return i_op.__get__(obj, type(obj))  # type: ignore

        self.bind_f = bind_f


def _l_to_r_op(op: F) -> F:
    """Swap the argument order to turn an l-op into an r-op."""

    def r_op(obj: t.Any, other: t.Any) -> t.Any:
        return op(other, obj)

    return t.cast(F, r_op)


def _identity(o: T) -> T:
    return o


class LocalProxy(t.Generic[T]):
    """
    LocalProxy 是一个代理对象，用于封装绑定到上下文局部对象的对象。代理对象上的所有操作都会转发到绑定的对象上。如果没有绑定对象，将会引发 RuntimeError。

    参数说明：
    local：提供被代理对象的上下文局部对象。
    name：代理被代理对象上的该属性。
    unbound_message：如果上下文局部对象未绑定，显示的错误消息。

    可以使用 LocalProxy 代理一个 ContextVar，以便更方便地访问。传递要代理的属性名。
    _request_var = ContextVar("request")
    request = LocalProxy(_request_var)
    session = LocalProxy(_request_var, "session")

    可以通过调用带有属性名的 Local 命名空间上的局部对象来代理一个属性。
    data = Local()
    user = data("user")

    可以通过调用 LocalStack 上的局部对象来代理该栈的顶部项。传递要代理的属性名。
    app_stack = LocalStack()
    current_app = app_stack()
    g = app_stack("g")

    可以传递一个函数来代理该函数的返回值
    session = LocalProxy(lambda: request.session)

    LocalProxy 会代理 __repr__ 和 __class__，所以 repr(x) 和 isinstance(x, cls) 看起来都像被代理的对象。
    可以使用 issubclass(type(x), LocalProxy) 检查对象是否为代理对象。
    """

    __slots__ = ("__wrapped", "_get_current_object")

    _get_current_object: t.Callable[[], T]

    def __init__(
            self,
            local: t.Union[ContextVar[T], Local, LocalStack[T], t.Callable[[], T]],
            name: t.Optional[str] = None,
            *,
            unbound_message: t.Optional[str] = None,
    ) -> None:
        if name is None:
            get_name = _identity
        else:
            get_name = attrgetter(name)  # type: ignore[assignment]

        if unbound_message is None:
            unbound_message = "object is not bound"

        if isinstance(local, Local):
            if name is None:
                raise TypeError("'name' is required when proxying a 'Local' object.")

            def _get_current_object() -> T:
                try:
                    return get_name(local)  # type: ignore[return-value]
                except AttributeError:
                    raise RuntimeError(unbound_message) from None

        elif isinstance(local, LocalStack):

            def _get_current_object() -> T:
                obj = local.top  # type: ignore[union-attr]

                if obj is None:
                    raise RuntimeError(unbound_message)

                return get_name(obj)

        elif isinstance(local, ContextVar):

            def _get_current_object() -> T:
                try:
                    obj = local.get()  # type: ignore[union-attr]
                except LookupError:
                    raise RuntimeError(unbound_message) from None

                return get_name(obj)

        elif callable(local):

            def _get_current_object() -> T:
                return get_name(local())  # type: ignore

        else:
            raise TypeError(f"Don't know how to proxy '{type(local)}'.")

        object.__setattr__(self, "_LocalProxy__wrapped", local)
        object.__setattr__(self, "_get_current_object", _get_current_object)

    __doc__ = _ProxyLookup(  # type: ignore
        class_value=__doc__, fallback=lambda self: type(self).__doc__, is_attr=True
    )
    __wrapped__ = _ProxyLookup(
        fallback=lambda self: self._LocalProxy__wrapped, is_attr=True
    )
    # __del__ should only delete the proxy
    __repr__ = _ProxyLookup(  # type: ignore
        repr, fallback=lambda self: f"<{type(self).__name__} unbound>"
    )
    __str__ = _ProxyLookup(str)  # type: ignore
    __bytes__ = _ProxyLookup(bytes)
    __format__ = _ProxyLookup()  # type: ignore
    __lt__ = _ProxyLookup(operator.lt)
    __le__ = _ProxyLookup(operator.le)
    __eq__ = _ProxyLookup(operator.eq)  # type: ignore
    __ne__ = _ProxyLookup(operator.ne)  # type: ignore
    __gt__ = _ProxyLookup(operator.gt)
    __ge__ = _ProxyLookup(operator.ge)
    __hash__ = _ProxyLookup(hash)  # type: ignore
    __bool__ = _ProxyLookup(bool, fallback=lambda self: False)
    __getattr__ = _ProxyLookup(getattr)
    # __getattribute__ triggered through __getattr__
    __setattr__ = _ProxyLookup(setattr)  # type: ignore
    __delattr__ = _ProxyLookup(delattr)  # type: ignore
    __dir__ = _ProxyLookup(dir, fallback=lambda self: [])  # type: ignore
    # __get__ (proxying descriptor not supported)
    # __set__ (descriptor)
    # __delete__ (descriptor)
    # __set_name__ (descriptor)
    # __objclass__ (descriptor)
    # __slots__ used by proxy itself
    # __dict__ (__getattr__)
    # __weakref__ (__getattr__)
    # __init_subclass__ (proxying metaclass not supported)
    # __prepare__ (metaclass)
    __class__ = _ProxyLookup(
        fallback=lambda self: type(self), is_attr=True
    )  # type: ignore
    __instancecheck__ = _ProxyLookup(lambda self, other: isinstance(other, self))
    __subclasscheck__ = _ProxyLookup(lambda self, other: issubclass(other, self))
    # __class_getitem__ triggered through __getitem__
    __call__ = _ProxyLookup(lambda self, *args, **kwargs: self(*args, **kwargs))
    __len__ = _ProxyLookup(len)
    __length_hint__ = _ProxyLookup(operator.length_hint)
    __getitem__ = _ProxyLookup(operator.getitem)
    __setitem__ = _ProxyLookup(operator.setitem)
    __delitem__ = _ProxyLookup(operator.delitem)
    # __missing__ triggered through __getitem__
    __iter__ = _ProxyLookup(iter)
    __next__ = _ProxyLookup(next)
    __reversed__ = _ProxyLookup(reversed)
    __contains__ = _ProxyLookup(operator.contains)
    __add__ = _ProxyLookup(operator.add)
    __sub__ = _ProxyLookup(operator.sub)
    __mul__ = _ProxyLookup(operator.mul)
    __matmul__ = _ProxyLookup(operator.matmul)
    __truediv__ = _ProxyLookup(operator.truediv)
    __floordiv__ = _ProxyLookup(operator.floordiv)
    __mod__ = _ProxyLookup(operator.mod)
    __divmod__ = _ProxyLookup(divmod)
    __pow__ = _ProxyLookup(pow)
    __lshift__ = _ProxyLookup(operator.lshift)
    __rshift__ = _ProxyLookup(operator.rshift)
    __and__ = _ProxyLookup(operator.and_)
    __xor__ = _ProxyLookup(operator.xor)
    __or__ = _ProxyLookup(operator.or_)
    __radd__ = _ProxyLookup(_l_to_r_op(operator.add))
    __rsub__ = _ProxyLookup(_l_to_r_op(operator.sub))
    __rmul__ = _ProxyLookup(_l_to_r_op(operator.mul))
    __rmatmul__ = _ProxyLookup(_l_to_r_op(operator.matmul))
    __rtruediv__ = _ProxyLookup(_l_to_r_op(operator.truediv))
    __rfloordiv__ = _ProxyLookup(_l_to_r_op(operator.floordiv))
    __rmod__ = _ProxyLookup(_l_to_r_op(operator.mod))
    __rdivmod__ = _ProxyLookup(_l_to_r_op(divmod))
    __rpow__ = _ProxyLookup(_l_to_r_op(pow))
    __rlshift__ = _ProxyLookup(_l_to_r_op(operator.lshift))
    __rrshift__ = _ProxyLookup(_l_to_r_op(operator.rshift))
    __rand__ = _ProxyLookup(_l_to_r_op(operator.and_))
    __rxor__ = _ProxyLookup(_l_to_r_op(operator.xor))
    __ror__ = _ProxyLookup(_l_to_r_op(operator.or_))
    __iadd__ = _ProxyIOp(operator.iadd)
    __isub__ = _ProxyIOp(operator.isub)
    __imul__ = _ProxyIOp(operator.imul)
    __imatmul__ = _ProxyIOp(operator.imatmul)
    __itruediv__ = _ProxyIOp(operator.itruediv)
    __ifloordiv__ = _ProxyIOp(operator.ifloordiv)
    __imod__ = _ProxyIOp(operator.imod)
    __ipow__ = _ProxyIOp(operator.ipow)
    __ilshift__ = _ProxyIOp(operator.ilshift)
    __irshift__ = _ProxyIOp(operator.irshift)
    __iand__ = _ProxyIOp(operator.iand)
    __ixor__ = _ProxyIOp(operator.ixor)
    __ior__ = _ProxyIOp(operator.ior)
    __neg__ = _ProxyLookup(operator.neg)
    __pos__ = _ProxyLookup(operator.pos)
    __abs__ = _ProxyLookup(abs)
    __invert__ = _ProxyLookup(operator.invert)
    __complex__ = _ProxyLookup(complex)
    __int__ = _ProxyLookup(int)
    __float__ = _ProxyLookup(float)
    __index__ = _ProxyLookup(operator.index)
    __round__ = _ProxyLookup(round)
    __trunc__ = _ProxyLookup(math.trunc)
    __floor__ = _ProxyLookup(math.floor)
    __ceil__ = _ProxyLookup(math.ceil)
    __enter__ = _ProxyLookup()
    __exit__ = _ProxyLookup()
    __await__ = _ProxyLookup()
    __aiter__ = _ProxyLookup()
    __anext__ = _ProxyLookup()
    __aenter__ = _ProxyLookup()
    __aexit__ = _ProxyLookup()
    __copy__ = _ProxyLookup(copy.copy)
    __deepcopy__ = _ProxyLookup(copy.deepcopy)
    # __getnewargs_ex__ (pickle through proxy not supported)
    # __getnewargs__ (pickle)
    # __getstate__ (pickle)
    # __setstate__ (pickle)
    # __reduce__ (pickle)
    # __reduce_ex__ (pickle)
