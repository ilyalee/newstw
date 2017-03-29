#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import unicodedata
import re
import arrow
import html
import settings
from hashlib import sha3_224
from urllib.parse import urlparse, parse_qs
from dateutil import parser
from string import whitespace


def dict_filter(keys, items):
    if not isiterable(keys):
        keys = clist(keys)
    if not isiterable(items):
        items = clist(items)
    return [{key: value for key, value in item.items() if key in keys} for item in items]


def dict_blocker(keys, items):
    if not isiterable(keys):
        keys = clist(keys)
    if not isiterable(items):
        items = clist(items)
    for key in keys:
        for item in items:
            del_key(key, True, item)
    return items


def dict_cleaner(value, items):
    return {key: value for key, value in items.items() if value}


def data_filter(text, keys, items):
    if not text:
        return items

    collect = []
    if not isiterable(keys):
        keys = clist(keys)

    pat = re.compile(text, re.UNICODE)
    seen = set()

    for item in items:
        founds = []
        item["founds"] = []
        for key in keys:
            if key in item:
                founds = re.findall(pat, item[key])
                if len(founds) > 0:
                    item["founds"] += founds
        if item["founds"]:
            item["founds"] = set(item["founds"])
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
    items = clist(items)
    if condition:
        targets = dict_filter([from_key], items)
        select_key = isinstance(condition, bool)
        if not select_key:
            value = fn(condition)
        for i in range(len(targets)):
            if select_key:
                if from_key in targets[i]:
                    obj = fn(targets[i][from_key])
            else:
                obj = value
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
        sources = (target[from_key] for target in targets if from_key in target)
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
        text = "".join(item[key] for key in keys if key in item)
        item[key] = githash(text.translate(dict.fromkeys(map(ord, whitespace))), hexdigest=True)
    return items


def data_cleaner(key, items):
    for item in items:
        if key in item:
            item[key] = clean_text(item[key])
    return items


def normalize_news(text):
    # return unicodedata.normalize("NFD", text)
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
    if not isiterable(formats):
        formats = clist(formats)
    for i, format in enumerate(formats):
        try:
            timetext = arrow.get(source, format).replace(tzinfo=tzinfo).format()
            return timetext
        except arrow.parser.ParserError as e:
            if i >= (len(formats) - 1):
                if __debug__:
                    data['debug'] = e
                return ''
            else:
                pass


def time_localizer(key, items):
    if not isiterable(items):
        items = clist(items)
    tzinfo = settings.TIMEZONE
    for item in items:
        if key in item:
            import datetime
            if isinstance(item[key], datetime.datetime):
                item[key] = arrow.get(item[key]).replace(tzinfo=tzinfo).format()
            elif isinstance(item[key], str):
                item[key] = arrow.get(parser.parse(item[key])).replace(tzinfo=tzinfo).format()
            else:
                raise arrow.parser.TzinfoParser("type missing")
    return items


def time_corrector(key, items):
    if not isiterable(items):
        items = clist(items)
    tzinfo = settings.TIMEZONE
    for item in items:
        if key in item:
            import datetime
            if isinstance(item[key], datetime.date):
                item[key] = arrow.get(item[key]).to(tzinfo).format()
            elif isinstance(item[key], str):
                item[key] = arrow.get(parser.parse(item[key])).to(tzinfo).format()
            else:
                raise arrow.parser.TzinfoParser("type missing")
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
    if all(key in item for item in items):
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


def keyword_builder(keywords):
    keyword_list = []
    if not keywords:
        return keyword_list

    if isinstance(keywords, str):
        keywords = keywords.split(",")

    for keyword in keywords:
        if " " in keyword:
            sub = keyword.split(" ")
            subp = (".*".join(map(str, comb)) for comb in itertools.permutations(sub))
            keyword_list.append('|'.join(subp))
        else:
            keyword_list.append(keyword)

    keyword_list = '|'.join(keyword_list)

    return keyword_list


def hightlight_keywords(value, keywords):
    if not keywords:
        return value
    if not isiterable(keywords):
        keywords = clist(keywords)

    for keyword in keywords:
        value = re.sub(f'({keyword})', f'<strong style="color: #E57373;">\g<1></strong>', value, flags=re.I)
    return value


def local_humanize(value):
    tzinfo = settings.TIMEZONE
    local = arrow.get(value).replace(tzinfo=tzinfo)
    return local.humanize(locale='zh_tw')


def isiterable(target):
    import collections
    return isinstance('ciao', collections.Iterator)


def clist(target):
    import types
    if isinstance(target, str):
        return [target]
    else:
        return list(target)
