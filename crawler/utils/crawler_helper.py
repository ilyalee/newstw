#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession

def fetch_news(url, encoding='utf-8'):
    output = {}
    r = requests.get(url)
    r.encoding = encoding
    r.close()
    html = clean_html(r.text)
    news = NewsDataProcessor(r.url, html)
    output = news.output()

    return output

def fetch_news_all(urls, encoding='utf-8', timeout=30):
    if isinstance(urls, list):
        return fetch_news_all_fast(urls, encoding, timeout)

def fetch_news_all_fast(urls, encoding, timeout):
    collect = []
    resopones = []
    session = FuturesSession(session=requests.Session(), executor=ThreadPoolExecutor(max_workers=os.cpu_count()))
    future_resps = [session.get(url, timeout=timeout) for url in urls]
    resopones = [future.result() for future in future_resps]
    for resp in resopones:
        resp.encoding = encoding
        html = clean_html(resp.text)
        news = NewsDataProcessor(resp.url, html)
        output = news.output()
        collect.append(output)
    session.close()

    return collect

def fetch_news_all_slow(urls, encoding, timeout):
    def _hook(*encoding):
        def hook(resp, **kwargs):
            resp.encoding = encoding
            return resp
        return hook

    import grequests
    collect = []
    resopones = []
    session = requests.session()
    rs = (grequests.get(url, session=session, timeout=timeout, hooks={'response': _hook(encoding)}) for url in urls)
    resopones = grequests.map(rs, size=len(urls), exception_handler=exception_handler)
    for resp in resopones:
        html = clean_html(resp.text)
        news = NewsDataProcessor(resp.url, html)
        output = news.output()
        collect.append(output)
    session.close()

    return collect

def exception_handler(request, exception):
    if __debug__:
        print("Request failed: %s") % exception
