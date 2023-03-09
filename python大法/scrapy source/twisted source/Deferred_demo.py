from twisted.internet import reactor, defer
from twisted.python import failure


def callback_func1(r):
    print('回调方法1: 结果=%s' % r)
    return r * r


def callback_func2(r):
    print('回调方法2: 传入结果=%s' % r)
    raise ValueError('value error')


def errback_func(f):
    print('错误回调:{}'.format(f))


d = defer.Deferred()
d.addCallback(callback_func1)
d.addCallback(callback_func2)

d.addErrback(errback_func)

d.callback(10)
