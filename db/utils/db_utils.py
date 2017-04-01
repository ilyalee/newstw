#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashids import Hashids
import settings
from utils.data_utils import datetime_encapsulator, data_updater, isiterable, clist


def load_as_objs(cls, items):
    return (cls(**item) for item in items)


def load_as_dicts(result_set):
    return (item.to_dict() for item in result_set)


def id2hashid(id):
    hashids = Hashids(salt=settings.SALT, min_length=5)
    hashid = hashids.encode(id)
    return hashid


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
    return (hashids.encode(id) for id in ids)


def sqlite_datetime_compatibility(keys):
    def _(func):
        def wrapper(*args, **kargs):
            import types
            nonlocal keys
            args = list(args)
            items = args[1]
            if not isiterable(keys):
                keys = clist(keys)
            if not isiterable(items):
                items = clist(items)
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
            if not isiterable(keys):
                keys = clist(keys)
            if not isiterable(items):
                items = clist(items)
            for key in keys:
                if all(key in item for item in items):
                    items = data_updater(key, key, list2str, True, items)
            args[1] = items
            result = func(*args, **kargs)
            return result
        return wrapper
    return _


def str2list(string, delimiter=','):
    if not string:
        return []
    return sorted(filter(None, string.split(delimiter)))


def list2str(lst, delimiter=','):
    if not lst:
        return None
    return delimiter.join(sorted(lst))


def reload_keyword(keyword):
    keywords = str2list(keyword, ',')
    if len(keywords) > 1:
        return (keywords, 'OR')
    keywords = str2list(keyword, ' ')
    if len(keywords) > 1:
        return (keywords, 'AND')
    keywords = str2list(keyword, '+')
    if len(keywords) > 1:
        return (keywords, 'AND')
    keywords = str2list(keyword, '|')
    if len(keywords) > 1:
        return (keywords, 'OR')
    else:
        return (keywords, 'OR')
