#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashids import Hashids
import settings
from utils.data_utils import datetime_encapsulator, data_updater


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
                items = data_updater(key, key, datetime_encapsulator, True, items)
            args[1] = items
            result = func(*args, **kargs)
            return result
        return wrapper
    return _


def list_as_str(keys):
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
                if all(key in item for item in items):
                    items = data_updater(key, key, list2str, True, items)
            args[1] = items
            result = func(*args, **kargs)
            return result
        return wrapper
    return _


def str2list(str):
    if not str:
        return []
    return str.split(",").sort()


def list2str(lst):
    if not lst:
        return None
    return ",".join(lst.sort())
