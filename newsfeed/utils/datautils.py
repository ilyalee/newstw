#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from functools import partial
from dateutil import parser
import arrow
import re, html
from urllib.parse import urlparse, parse_qs

def dictFilter(keys, items):
    #return [*map(partial(_filterKeys, keys), items)]
    return [{k: v for k, v in item.items() if k in keys} for item in items]

def timeCorrector(key, items):
    #return [*map(partial(_updateTime, key), items)]
    for item in items:
        if key in item:
            item[key] = arrow.get(parser.parse(item[key])).format()
    return items

def linkCorrector(key, items):
    for item in items:
        if key in item:
            o = urlparse(item[key])
            q = parse_qs(o.query)
            if 'url' in q:
                item[key] = q['url']
    return items

def dataCleaner(key, items):
    #return [*map(partial(partial(_updateText, cleanText), key), items)]
    for item in items:
        if key in item:
            item[key] = cleanText(item[key])
    return items

def dataFilter(text, keys, items):
    if not text: return items

    collect = []
    if isinstance(keys, str):
        keys = [keys]
    pat = re.compile(text, re.UNICODE)
    seen = set()
    for i in range(len(items)):
        for key in keys:
            if key in items[i]:
                found = re.search(pat, items[i][key])
                if found and (i not in seen and not seen.add(i)):
                    collect.append(items[i])
    return collect

def dataInserter(val, key, items):
    if val:
        for item in items:
            item[key] = val
    return items

def dataUpdater(key, sKey, fn, go, items):
    if go:
        targets = dictFilter([sKey], items)
        for i in range(len(targets)):
            obj = fn(targets[i][sKey])
            if key in obj:
                items[i][key] = obj[key]
    return items

def dataUpdaterAll(key, sKey, fn, go, items):
    if go:
        targets = dictFilter([sKey], items)
        sources = [target[sKey] for target in targets if sKey in target]
        objs = fn(sources)
        for i in range(len(objs)):
            items[i][key] = objs[i][key]
    return items

def cleanText(text):
    pat = re.compile(r'(<!--.*?-->|<[^>]*>)')
    text = pat.sub('', text)
    text = html.escape(text)
    # remove all newlines
    text = re.sub(r"\n", "", text)
    text = text.strip(' ')
    return text
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
