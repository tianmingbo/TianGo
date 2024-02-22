from functools import partial
import typing as t


class C:
    d = 'dafaf'


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
                print(obj)
                return partial(f, obj)  # 绑定f函数的第一个参数obj

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
        """
        __get__ 是一个特殊的方法（也称为描述符方法），在 Python 中用于实现描述符协议（Descriptor Protocol）。
        描述符是一种类属性机制，允许你自定义类的属性访问行为。

        __get__ 方法在属性获取（访问）时被调用。它接受三个参数：
            self: 描述符实例自身。
            instance: 要访问属性的实例对象（如果通过实例访问属性）。
            owner: 拥有属性的类对象。
        """
        if instance is None:
            if self.class_value is not None:
                return self.class_value

            return self

        try:
            obj = C()
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


class A:
    __getattr__ = _ProxyLookup(getattr)


a = A()
print(a.d)
