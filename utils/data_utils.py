#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from functools import partial
import unicodedata
import re
import arrow
import html
import settings
from hashlib import sha3_224
from urllib.parse import urlparse, parse_qs
from dateutil import parser


def dict_filter(keys, items):
    if not isinstance(keys, list):
        keys = [keys]
    if not isinstance(items, list):
        items = [items]
    return [{key: value for key, value in item.items() if key in keys} for item in items]


def dict_blocker(keys, items):
    if not isinstance(keys, list):
        keys = [keys]
    if not isinstance(items, list):
        items = [items]
    for key in keys:
        for item in items:
            del_key(key, True, item)
    return items


def data_filter(text, keys, items):
    if not text:
        return items

    collect = []
    if isinstance(keys, str):
        keys = [keys]
    pat = re.compile(text, re.UNICODE)

    seen = set()
    for i, item in enumerate(items):
        for key in keys:
            if key in item:
                found = re.search(pat, item[key])
                if found and (i not in seen and not seen.add(i)):
                    collect.append(item)
    return collect


def data_inserter(val, key, items):
    if val:
        for item in items:
            item[key] = val
    return items


def data_remover(val, key, items):
    return [item for item in items if key in item and item[key] != val]


def data_updater(key, from_key, fn, condition, items):
    if condition:
        targets = dict_filter([from_key], items)
        select = isinstance(condition, bool)
        for i in range(len(targets)):
            if select:
                obj = targets[i][from_key]
            else:
                obj = fn(condition)
            items[i][key] = obj
    return items


def data_kv_updater(key, from_key, fn, go, items):
    if go:
        targets = dict_filter([from_key], items)
        for i in range(len(targets)):
            obj = fn(targets[i][from_key])
            items[i][key] = obj[key]
    return items


def data_kv_updater_all_load(from_key, fn, go, items):
    remote_items = []
    if go:
        targets = dict_filter([from_key], items)
        sources = [target[from_key] for target in targets if from_key in target]
        remote_items = fn(sources)
    return remote_items


def data_kv_updater_all_by_remote_items(remote_items, key, from_key, fn, go, items):
    if go:
        for i in range(len(remote_items)):
            new_val = remote_items[i][key]
            if new_val:
                items[i][key] = new_val
    return items


def data_kv_updater_all(key, from_key, fn, go, items):
    if go:
        remote_items = data_kv_updater_all_load(from_key, fn, go, items)
        items = data_kv_updater_all_by_remote_items(remote_items, key, from_key, fn, go, items)
    return items


def data_hasher(key, keys, items):
    for item in items:
        text = "".join([item[key] for key in keys if key in item])
        item[key] = githash(text.replace(" ", ""), hexdigest=True)
    return items


def data_cleaner(key, items):
    # return [*map(partial(partial(_update_text, clean_text), key), items)]
    for item in items:
        if key in item:
            item[key] = clean_text(item[key])
    return items


def normalize_news(text):
    #return unicodedata.normalize("NFD", text)
    return text

def trim_data_val(key, trimtext, data):
    if isinstance(trimtext, str) and key in data:
        data[key] = re.sub(u'%s$' % trimtext, '', data[key])


def del_key(key, ok, data):
    if not isinstance(data, dict):
        return
    if ok:
        data.pop(key, None)


def datetime_encapsulator(datetime_str):
    return arrow.get(datetime_str).datetime


def localize_datetime(source, formats, tzinfo, data):
    if not isinstance(formats, list):
        formats = [formats]
    for i, format in enumerate(formats):
        try:
            timetext = arrow.get(source, format).replace(tzinfo=tzinfo).format()
            return timetext
        except arrow.parser.ParserError as err:
            if i >= (len(formats) - 1):
                if __debug__:
                    data['debug'] = err
                return ''
            else:
                pass


def time_corrector(key, items):
    if not isinstance(items, list):
        items = [items]
    # return [*map(partial(_update_time, key), items)]
    tzinfo = settings.TIMEZONE
    for item in items:
        if key in item:
            import datetime
            if isinstance(item[key], datetime.date):
                item[key] = arrow.get(item[key]).replace(tzinfo=tzinfo).format()
            elif isinstance(item[key], str):
                item[key] = arrow.get(parser.parse(item[key])).replace(tzinfo=tzinfo).format()
    return items


def normalize_link(link):
    o = urlparse(link)
    q = parse_qs(o.query)
    if 'url' in q:
        link = q['url'][0]

    while link.endswith('//'):
        link = re.sub('//$', '/', link)
    return link


def link_corrector(key, items):
    for item in items:
        item[key] = normalize_link(item[key])
    return items


def clean_text(text):
    pat = re.compile(r'(<!--.*?-->|<[^>]*>)')
    text = pat.sub('', text)
    text = html.escape(text)
    pat = re.compile('<.*?>')
    text = pat.sub('', text)
    # remove all newlines
    text = re.sub(r"\n", "", text)
    text = text.strip(' ')
    text = text.replace("\u3000", " ")
    text = text.replace("&amp;nbsp;", "")
    return text

# ref: http://stackoverflow.com/questions/552659/how-to-assign-a-git-sha1s-to-a-file-without-git
def githash(data, hexdigest=False):
    s = sha3_224()
    s.update("blob %u\0".encode('utf-8') % len(data))
    s.update(str(data).encode('utf-8'))
    if hexdigest:
        return s.hexdigest()
    else:
        return s.digest()


def fb_time_to_local(key, tzinfo, items):
    for item in (item for item in items if key in item):
        item[key] = arrow.get(item[key]).replace(tzinfo=tzinfo).format()
    return items


'''
def _filter_keys(keys, item):
    #return dict(filter(lambda _obj: _obj[0] in keys, obj.items()))
    return {key: value for key, value in item.items() if key in keys}
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
