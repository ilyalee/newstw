#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashids import Hashids
import settings
from utils.data_utils import datetime_encapsulator, data_updater
import asyncio
import os
import functools
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def load_as_objs(cls, items):
    return [cls(**item) for item in items]


def decoded_hashid(func):
    hashids = Hashids(salt=settings.SALT, min_length=5)

    def wrapper(*args, **kargs):
        args = list(args)
        (args[1],) = hashids.decode(args[1])
        result = func(*args, **kargs)
        return result
    return wrapper


def encoded_hashid(func):
    hashids = Hashids(salt=settings.SALT, min_length=5)
    def wrapper(*args, **kargs):
        args = list(args)
        args[1] = hashids.encode(args[1])
        result = func(*args, **kargs)
        return result
    return wrapper


def encode_hashid_list(ids):
    hashids = Hashids(salt=settings.SALT, min_length=5)
    return [hashids.encode(id) for id in ids]


def sqlite_datetime_compatibility(keys):
    def _(func):
        def wrapper(*args, **kargs):
            nonlocal keys
            args = list(args)
            items = args[1]
            if not isinstance(items, list):
                items = [items]
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                items = data_updater("published", "published", datetime_encapsulator, True, items)
            args[1] = items
            result = func(*args, **kargs)
            return result
        return wrapper
    return _


def as_run(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(os.cpu_count())
    future = loop.run_in_executor(executor, functools.partial(func, *args, **kwargs))
    return asyncio.ensure_future(future)


def as_run_pro(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(os.cpu_count())
    future = loop.run_in_executor(executor, functools.partial(func, *args, **kwargs))
    return asyncio.ensure_future(future)
