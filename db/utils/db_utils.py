#!/usr/bin/env python
# -*- coding: utf-8 -*-


def load_as_objs(cls, items):
    return [cls(**item) for item in items]
