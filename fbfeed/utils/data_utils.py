#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import arrow
from hashlib import sha1


# ref: http://stackoverflow.com/questions/552659/how-to-assign-a-git-sha1s-to-a-file-without-git
def githash(data, hexdigest=False):
    s = sha1()
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


def dict_filter(keys, items):
    return [{k: v for k, v in item.items() if k in keys} for item in items]


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


def data_hasher(key, keys, items):
    text = "".join(item[key] for key in keys for item in items)
    for item in items:
        item[key] = githash(text, hexdigest=True)
    return items


def data_cleaner(key, items):
    for item in items:
        if key in item:
            item[key] = clean_text(item[key])
    return items


def clean_text(text):
    text = re.sub(r"\n", "", text)
    text = text.strip(' ')
    return text
