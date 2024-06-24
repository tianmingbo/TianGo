import sys

_PENDING = 'PENDING'
_CANCELLED = 'CANCELLED'
_FINISHED = 'FINISHED'


class Future:
    """
    Future 实例有以下三个属性非常重要
    _state: 运行状态，有三种，分别是 PENDING（正在运行）、CANCELLED（已取消）、FINISHED（已完成）
    _result: future 完成之后的设置的结果
    _exception: future 报错时设置的异常
    """

    # Class variables serving as defaults for instance variables.
    _state = _PENDING
    _result = None
    _exception = None
    _loop = None
    _source_traceback = None
    _cancel_message = None
    # A saved CancelledError for later chaining as an exception context.
    _cancelled_exc = None

    # This field is used for a dual purpose:
    # - Its presence is a marker to declare that a class implements
    #   the Future protocol (i.e. is intended to be duck-type compatible).
    #   The value must also be not-None, to enable a subclass to declare
    #   that it is not compatible by setting this to None.
    # - It is set by __iter__() below so that Task._step() can tell
    #   the difference between
    #   `await Future()` or`yield from Future()` (correct) vs.
    #   `yield Future()` (incorrect).
    _asyncio_future_blocking = False

    __log_traceback = False

    def __init__(self, *, loop=None):
        """Initialize the future.

        The optional event_loop argument allows explicitly setting the event
        loop object used by the future. If it's not provided, the future uses
        the default event loop.
        """
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop
        self._callbacks = []
        if self._loop.get_debug():
            self._source_traceback = format_helpers.extract_stack(
                sys._getframe(1))

    _repr_info = base_futures._future_repr_info

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__,
                                ' '.join(self._repr_info()))

    def __del__(self):
        if not self.__log_traceback:
            # set_exception() was not called, or result() or exception()
            # has consumed the exception
            return
        exc = self._exception
        context = {
            'message':
                f'{self.__class__.__name__} exception was never retrieved',
            'exception': exc,
            'future': self,
        }
        if self._source_traceback:
            context['source_traceback'] = self._source_traceback
        self._loop.call_exception_handler(context)

    def __class_getitem__(cls, type):
        return cls

    @property
    def _log_traceback(self):
        return self.__log_traceback

    @_log_traceback.setter
    def _log_traceback(self, val):
        if bool(val):
            raise ValueError('_log_traceback can only be set to False')
        self.__log_traceback = False

    def get_loop(self):
        """Return the event loop the Future is bound to."""
        loop = self._loop
        if loop is None:
            raise RuntimeError("Future object is not initialized.")
        return loop

    def _make_cancelled_error(self):
        """Create the CancelledError to raise if the Future is cancelled.

        This should only be called once when handling a cancellation since
        it erases the saved context exception value.
        """
        if self._cancel_message is None:
            exc = exceptions.CancelledError()
        else:
            exc = exceptions.CancelledError(self._cancel_message)
        exc.__context__ = self._cancelled_exc
        # Remove the reference since we don't need this anymore.
        self._cancelled_exc = None
        return exc

    def cancel(self, msg=None):
        # cancel 方法，负责取消一个 future
        # 并且该方法有返回值，取消成功返回 True，取消失败返回 False
        self.__log_traceback = False
        # 检测状态是否为 PENDING，不是 PENDING，说明 future 已经运行完毕或取消了
        # 那么返回 False 表示取消失败，但对于 future 而言则无影响
        if self._state != _PENDING:
            return False
        # 如果状态是 PENDING，那么将其改为 CANCELLED
        self._state = _CANCELLED
        self.__schedule_callbacks()
        return True

    def __schedule_callbacks(self):
        """Internal: Ask the event loop to call all callbacks.

        The callbacks are scheduled to be called as soon as possible. Also
        clears the callback list.
        """
        callbacks = self._callbacks[:]
        if not callbacks:
            return

        self._callbacks[:] = []
        for callback, ctx in callbacks:
            self._loop.call_soon(callback, self, context=ctx)

    def cancelled(self):
        # 判断 future 是否被取消，那么检测它的状态是否为 CANCELLED 即可
        return self._state == _CANCELLED

    # Don't implement running(); see http://bugs.python.org/issue18699

    def done(self):
        # 判断 future 是否已经完成，那么检测它的状态是否不是 PENDING 即可
        # 注意：CANCELLED 和 FINISHED 都表示已完成
        return self._state != _PENDING

    def result(self):
        # 调用 result 方法相当于获取 future 设置的结果
        # 但如果它的状态为 CANCELLED，表示取消了，那么抛出 CancelledError
        # 正如同你 await 一个已取消的任务一样，因为 await 会阻塞任务并拿到它的执行结果
        # 如果任务已取消，同样抛出 CancelledError
        # 所以 future 和 task 是很相似的，因为 Task 本身就是 Future 的子类
        # 至于 Future 和 Task 具体的区别，我们一会儿再说
        if self._state == _CANCELLED:
            exc = self._make_cancelled_error()
            raise exc
        # 如果状态不是 FINISHED（说明还没有设置结果），那么抛出 asyncio.InvalidStateError 异常
        # 所以我们不能在 set_result 之前调用 result
        if self._state != _FINISHED:
            raise exceptions.InvalidStateError('Result is not ready.')
        self.__log_traceback = False
        # 走到这里说明状态为 FINISHED
        # 但不管是正常执行、还是出现异常，都会将状态标记为 FINISHED
        # 如果是出现异常，那么调用 result 会将异常抛出来
        if self._exception is not None:
            raise self._exception
        # 否则返回设置的结果
        return self._result

    def exception(self):
        # 无论是正常执行结束，还是出现异常，future 的状态都是已完成
        # 如果是正常执行结束，那么 self._result 就是结果，self._exception 为 None
        # 如果是出现异常，那么 self._result 为 None，self._exception 就是异常对象本身

        # 因此调用 result 和 exception 都要求 future 的状态为 FINISHED
        # 如果为 CANCELLED，那么同样抛出 CancelledError
        if self._state == _CANCELLED:
            exc = self._make_cancelled_error()
            raise exc
        # 如果为 PENDING，那么抛出 asyncio.InvalidStateError 异常
        if self._state != _FINISHED:
            raise exceptions.InvalidStateError('Exception is not set.')
        self.__log_traceback = False
        # 返回异常本身
        # 因此如果你不确定 future 到底是正常执行结束，还是抛了异常
        # 那么可以先调用 future.exception()，如果为 None，说明正常执行，再通过 future.result() 获取结果
        # 如果 future.exception() 不为 None，那么拿到的就是异常本身
        return self._exception

    def add_done_callback(self, fn, *, context=None):
        """Add a callback to be run when the future becomes done.

        The callback is called with a single argument - the future object. If
        the future is already done when this is called, the callback is
        scheduled with call_soon.
        """
        if self._state != _PENDING:
            self._loop.call_soon(fn, self, context=context)
        else:
            if context is None:
                context = contextvars.copy_context()
            self._callbacks.append((fn, context))

    # New method not in PEP 3148.

    def remove_done_callback(self, fn):
        """Remove all instances of a callback from the "call when done" list.

        Returns the number of callbacks removed.
        """
        filtered_callbacks = [(f, ctx)
                              for (f, ctx) in self._callbacks
                              if f != fn]
        removed_count = len(self._callbacks) - len(filtered_callbacks)
        if removed_count:
            self._callbacks[:] = filtered_callbacks
        return removed_count

    # So-called internal methods (note: no set_running_or_notify_cancel()).

    def set_result(self, result):
        # 当 future 正常执行结束时，会通过 set_result 设置结果
        # 显然在设置结果的时候，future 的状态应该为 PENDING
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'{self._state}: {self!r}')
        # 然后设置 self._result，当程序调用 future.result() 时会返回 self._result
        self._result = result
        # 并将状态标记为 FINISHED，表示一个任务从 PENDING 变成了 FINISHED
        # 所以我们不能对一个已完成的 future 再次调用 set_result
        # 因为第二次调用 set_result 的时候，状态已经不是 PENDING 了
        self._state = _FINISHED
        self.__schedule_callbacks()

    def set_exception(self, exception):
        # 设置异常时，状态应该为pending，不应该为canceled和finished
        if self._state != _PENDING:
            raise exceptions.InvalidStateError(f'{self._state}: {self!r}')
        # 但 exception 必须是异常，且不能是 StopIteration 异常
        if isinstance(exception, type):
            exception = exception()
        if type(exception) is StopIteration:
            raise TypeError("StopIteration interacts badly with generators "
                            "and cannot be raised into a Future")
        # 将 self._exception 设置为 exception
        # 调用 future.exception() 的时候，会返回 self._exception
        self._exception = exception
        self._state = _FINISHED
        # 将状态标记为已完成
        self.__schedule_callbacks()
        self.__log_traceback = True

    def __await__(self):
        if not self.done():
            self._asyncio_future_blocking = True
            yield self  # This tells Task to wait for completion.
        if not self.done():
            raise RuntimeError("await wasn't used with future")
        return self.result()  # May raise too.

    __iter__ = __await__  # make compatible with 'yield from'.
