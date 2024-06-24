from functools import wraps


def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # 预激生成器
        return gen  # 返回生成器

    return primer
