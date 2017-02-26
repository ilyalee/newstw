#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import grequests
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html

def fetch_news(url, encoding='utf-8'):
    output = {}
    r = requests.get(url)
    r.encoding = encoding
    r.close()
    html = clean_html(r.text)
    news = NewsDataProcessor(r.url, html)
    output = news.output()

    return output

def fetch_news_all(urls, encoding='utf-8'):
    collect = []
    resopones = []
    if isinstance(urls, list):
        session=requests.session()
        rs = (grequests.get(url, session=session, hooks={'response': _hook(encoding)}) for url in urls)
        resopones = grequests.map(rs, size=20, exception_handler=exception_handler)
        for r in resopones:
            html = clean_html(r.text)
            news = NewsDataProcessor(r.url, html)
            output = news.output()
            collect.append(output)
        session.close()

    return collect

def _hook(*encoding):
    def hook(r, **kwargs):
        r.encoding = encoding
        return r
    return hook

def exception_handler(request, exception):
    if __debug__:
        print("Request failed: %s") % exception
