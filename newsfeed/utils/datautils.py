#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from functools import partial
from dateutil import parser
import arrow
import re

def dictFilter(keys, items):
    #return [*map(partial(_filterKeys, keys), items)]
    return [{k: v for k, v in item.items() if k in keys} for item in items]

def timeCorrector(key, items):
    #return [*map(partial(_updateTime, key), items)]
    for item in items:
        item[key] = arrow.get(parser.parse(item[key])).format()
    return items

def dataCleaner(key, items):
    #return [*map(partial(partial(_updateText, cleanText), key), items)]
    for item in items:
        item[key] = cleanText(item[key])
    return items

def dataFilter(text, keys, items):
    found = []
    if isinstance(keys, list):
        pat = re.compile(text, re.UNICODE)
        inds = []
        for i in range(len(items)):
            match = None
            if i not in inds:
                for key in keys:
                    match = re.search(pat, items[i][key])
                    if match:
                        break
            if match:
                found.append(items[i])
                if i not in inds: inds.append(i)
    return found

def dataInsert(val, key, items):
    for item in items:
        item[key] = val
    return items

def cleanText(text):
    # remove all newlines
    text = re.sub(r"\n", "", text)

    #remove all img tag
    pat = re.compile(r"<img[\s\S]+?>", re.MULTILINE)
    text = re.sub(pat, "", text)

    return text.strip(' ')
'''
def _filterKeys(keys, item):
    #return dict(filter(lambda d: d[0] in keys, obj.items()))
    return {k: v for k, v in item.items() if k in keys}
'''
'''
def _updateTime(key, item):
    item.__setitem__(key, arrow.get(parser.parse(item[key])).format())
    return item
'''
'''
def _updateText(key, item):
    item.__setitem__(key, cleanText(item[key]))
    return item
'''
'''
def _updateText(fn, key, item):
    item.__setitem__(key, fn(item[key]))
    return item
'''
