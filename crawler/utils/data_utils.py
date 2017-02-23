#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import re
import arrow

def normalize_news(text):
    return unicodedata.normalize("NFKD", text)

def trim_data_val(key, trimtext, data):
    if isinstance(trimtext, str) and key in data:
        data[key] = re.sub(u'%s$' % trimtext, '', data[key])

def del_key(key, ok, data):
    if ok:
        data.pop(key, None)

def fix_datetime(source, formats, tzinfo, data):
    if isinstance(formats, str):
        formats = [formats]
    for i in range(len(formats)):
        try:
            timetext = arrow.get(source, formats[i]).replace(tzinfo=tzinfo).format()
            return timetext
        except arrow.parser.ParserError as err:
            if i >= (len(formats) - 1):
                if __debug__:
                    data['debug'] = err
                return ''
            else:
                continue
