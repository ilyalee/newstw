#!/usr/bin/env python
# -*- coding: utf-8 -*-


def debug_testing_mode():
    import settings
    return __debug__ and settings.TESTING
