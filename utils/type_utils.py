#!/usr/bin/env python
# -*- coding: utf-8 -*-


def ignore_except(IgnoreException=Exception, default=None):
    def _(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except IgnoreException:
                return default
        return wrapper
    return _


def sint(value, default=None):
    return ignore_except(ValueError, default)(int)(value)
