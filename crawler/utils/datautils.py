#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import re

def normalizeNews(text):
    return unicodedata.normalize("NFKD", text)

def trimDataVal(key, trimtext, data):
    if isinstance(trimtext, str) and key in data:
        data[key] = re.sub(u'%s$' % trimtext, '', data[key])

def delKey(key, ok, data):
    if ok:
        data.pop(key, None)
