#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashids import Hashids
import settings

def load_as_objs(cls, items):
    return [cls(**item) for item in items]

def decode_hashid(func):
    hashids = Hashids(salt=settings.SALT, min_length=5)
    def wrapper(*args, **kargs):
        args = list(args)
        (args[1],) = hashids.decode(args[1])
        result = func(*args, **kargs)
        return result
    return wrapper

def encode_hashid(func):
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
