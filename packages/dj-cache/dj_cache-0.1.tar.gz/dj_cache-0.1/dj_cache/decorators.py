import functools
from .models import Cache


def cached(ttl_seconds: int = None, *args, **kwargs):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            return Cache.get_or_set(func, ttl=ttl_seconds, *func_args, **func_kwargs)
        return wrapper
    return inner
