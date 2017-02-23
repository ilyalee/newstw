#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import arrow

def FBTimeToLocal(key, tzinfo, items):
    for item in (item for item in items if key in item):
        item[key] = arrow.get(item[key]).replace(tzinfo=tzinfo).format()
    return items

def dictFilter(keys, items):
    return [{k: v for k, v in item.items() if k in keys} for item in items]

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

def dataCleaner(key, items):
    for item in items:
        if key in item:
            item[key] = cleanText(item[key])
    return items

def cleanText(text):
    text = re.sub(r"\n", "", text)
    text = text.strip(' ')
    return text
