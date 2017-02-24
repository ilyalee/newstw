#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from functools import partial
from dateutil import parser
import arrow
import re
import html
from hashlib import sha3_224
from urllib.parse import urlparse, parse_qs
from itertools import chain

# ref: http://stackoverflow.com/questions/552659/how-to-assign-a-git-sha1s-to-a-file-without-git
def githash(data, hexdigest=False):
    s = sha3_224()
    s.update("blob %u\0".encode('utf-8') % len(data))
    s.update(str(data).encode('utf-8'))
    if hexdigest:
        return s.hexdigest()
    else:
        return s.digest()


def dict_filter(keys, items):
    # return [*map(partial(_filter_keys, keys), items)]
    return [{k: v for k, v in item.items() if k in keys} for item in items]


def time_corrector(key, items):
    # return [*map(partial(_update_time, key), items)]
    for item in items:
        if key in item:
            item[key] = arrow.get(parser.parse(item[key])).format()
    return items


def link_corrector(key, items):
    for item in items:
        if key in item:
            o = urlparse(item[key])
            q = parse_qs(o.query)
            if 'url' in q:
                item[key] = q['url']
    return items


def data_cleaner(key, items):
    # return [*map(partial(partial(_update_text, clean_text), key), items)]
    for item in items:
        if key in item:
            item[key] = clean_text(item[key])
    return items


def data_filter(text, keys, items):
    if not text:
        return items

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


def data_inserter(val, key, items):
    if val:
        for item in items:
            item[key] = val
    return items


def data_updater(key, sKey, fn, go, items):
    if go:
        targets = dict_filter([sKey], items)
        for i in range(len(targets)):
            obj = fn(targets[i][sKey])
            if key in obj:
                items[i][key] = obj[key]
    return items


def data_updater_all(key, sKey, fn, go, items):
    if go:
        targets = dict_filter([sKey], items)
        sources = [target[sKey] for target in targets if sKey in target]
        objs = fn(sources)
        for i in range(len(objs)):
            items[i][key] = objs[i][key]
    return items


def data_hasher(key, keys, items):
    for item in items:
        text = "".join([item[key] for key in keys if key in item])
        item[key] = githash(text, hexdigest=True)
    return items


def clean_text(text):
    pat = re.compile(r'(<!--.*?-->|<[^>]*>)')
    text = pat.sub('', text)
    text = html.escape(text)
    # remove all newlines
    text = re.sub(r"\n", "", text)
    text = text.strip(' ')
    return text
'''
def _filter_keys(keys, item):
    #return dict(filter(lambda d: d[0] in keys, obj.items()))
    return {k: v for k, v in item.items() if k in keys}
'''
'''
def _update_time(key, item):
    item.__setitem__(key, arrow.get(parser.parse(item[key])).format())
    return item
'''
'''
def _update_text(key, item):
    item.__setitem__(key, clean_text(item[key]))
    return item
'''
'''
def _update_text(fn, key, item):
    item.__setitem__(key, fn(item[key]))
    return item
'''
