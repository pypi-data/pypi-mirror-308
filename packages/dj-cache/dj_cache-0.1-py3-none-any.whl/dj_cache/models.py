import concurrent.futures
import os
from collections.abc import Callable
import typing
import functools
import threading
import pickle
import inspect
from datetime import timedelta

import logging
from django.db import models
from django.db.models import BinaryField, BigIntegerField
from django.utils.timezone import now
import concurrent.futures


executor: typing.Optional[concurrent.futures.ThreadPoolExecutor] = None

logger = logging.getLogger(__name__)

MAX_WORKERS = os.cpu_count() * 2


_LOCK_CREATOR = threading.Lock()  # we don't accidentally want to create multiple locks for the same key.
_KEY_LOCKS: typing.Dict[typing.Tuple, threading.Lock] = {}  # store the locks per key. Note: this can explode quite a bit.


def make_key(obj, typed=True):
    fn, args, kwargs = obj
    module = inspect.getmodule(fn)
    if module is None:
        module_name = "__main__"
    else:
        module_name = module.__name__
    full_name = module_name + "." + fn.__name__

    key = (full_name, tuple(args), tuple(sorted(kwargs.items())))
    if typed:
        key += tuple(type(v) for v in args)
        key += tuple(type(v) for _, v in sorted(kwargs.items()))
    return key


class Cache(models.Model):
    key = BinaryField(db_index=True)
    value = BinaryField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated_at = models.DateTimeField(auto_now=True, db_index=True)

    DEFAULT_TTL_SECONDS = 0

    ttl_seconds = models.BigIntegerField(
        default=int(timedelta(seconds=DEFAULT_TTL_SECONDS).total_seconds()),
        db_index=True,
    )

    @staticmethod
    def get_or_set(fn, ttl=None, *args, **kwargs):
        key = make_key((fn, args, kwargs))

        key_serialized = pickle.dumps(key, protocol=pickle.HIGHEST_PROTOCOL)
        logger.debug(f"Serialized: {str((key, key_serialized))}")

        stored: typing.Optional['Cache'] = Cache.objects.filter(key=key_serialized).select_for_update().first()
        if stored is None:
            value = fn(*args, **kwargs)
            value_serialized = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
            Cache.objects.create(key=key_serialized, value=value_serialized, ttl_seconds=ttl or Cache.DEFAULT_TTL_SECONDS)
            return value

        value_deserialized = pickle.loads(stored.value)
        # Check if stored value is expired.
        expires_at = stored.last_updated_at + timedelta(seconds=stored.ttl_seconds or Cache.DEFAULT_TTL_SECONDS)
        expired = now() > expires_at
        if not expired:
            logger.debug("Key is still fresh. Returning deserialized value.")
            return value_deserialized

        # Expired. May need to update.
        with _LOCK_CREATOR:
            if key not in _KEY_LOCKS:
                _KEY_LOCKS[key] = threading.Lock()

        _key_lock = _KEY_LOCKS[key]

        # Key has already been requested a cache update.
        if _key_lock.locked():
            logger.debug("Key is expired but a cache update is queued so will just return last stored value.")
            return value_deserialized

        # Hold the key-lock while the cache update runs.
        _key_lock.acquire()
        logger.debug("Key is expired. Submitting function to executor.")
        global executor
        if executor is None:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

        fut = executor.submit(fn, *args, **kwargs)
        fut.add_done_callback(
            functools.partial(
                _serialize_value_and_update_cache,
                stored=stored,
                lock=_key_lock,
            )
        )
        return value_deserialized


def _serialize_value_and_update_cache(result: concurrent.futures.Future, stored, lock):
    try:
        logger.debug("Function evaluation complete. Updating cache...")
        value_serialized = pickle.dumps(result.result(), protocol=pickle.HIGHEST_PROTOCOL)
        stored.value = value_serialized
        stored.last_updated_at = now()
        stored.save()
        logger.debug("Cache update complete...")
    finally:
        # Release the lock in all cases,
        # so future cache invalidations can be attempted.
        lock.release()
