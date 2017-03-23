#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html
from utils.async_utils import as_run
import requests


def fetch_news(url, encoding='utf-8', timeout=120):
    session = requests.session()
    output = {}
    r = session.get(url=url, timeout=timeout)
    r.encoding = encoding
    session.close()
    html = clean_html(r.text)
    return NewsDataProcessor(r.url, html).output()

async def as_fetch_news(url, encoding='utf-8', timeout=120):
    session = requests.session()
    resp = await as_run()(session.get)(url, timeout=timeout)
    resp.encoding = encoding
    session.close()
    html = clean_html(resp.text)
    return await NewsDataProcessor(resp.url, html).as_output()


def fetch_news_all(urls, encoding='utf-8', timeout=120):
    if isinstance(urls, list):
        return fetch_news_all_v2(urls, encoding, timeout)


def fetch_news_all_v2(urls, encoding, timeout):
    from concurrent.futures import ThreadPoolExecutor
    from requests_futures.sessions import FuturesSession

    collect = []
    resopones = []
    session = FuturesSession(session=requests.Session(),
                             executor=ThreadPoolExecutor(max_workers=os.cpu_count()))
    future_resps = [session.get(url, timeout=timeout, headers={
                                'Connection': 'close'}) for url in urls]
    resopones = [future.result() for future in future_resps]
    for resp in resopones:
        resp.encoding = encoding
        html = clean_html(resp.text)
        news = NewsDataProcessor(resp.url, html)
        output = news.output()
        collect.append(output)
    session.close()

    return collect


def fetch_news_all_v1(urls, encoding, timeout):
    import grequests

    def _hook(*encoding):
        def hook(resp, **kwargs):
            resp.encoding = encoding
            return resp
        return hook

    collect = []
    resopones = []
    session = requests.session()
    rs = (grequests.get(url, session=session, timeout=timeout, headers={
          'Connection': 'close'}, hooks={'response': _hook(encoding)}) for url in urls)
    resopones = grequests.map(rs, size=len(urls), exception_handler=exception_handler)
    for resp in resopones:
        html = clean_html(resp.text)
        news = NewsDataProcessor(resp.url, html)
        output = news.output()
        collect.append(output)
    session.close()

    return collect


def fetch_news_all_v0(urls, encoding, timeout):
    collect = []
    resopones = []
    session = requests.session()
    resopones = [session.get(url=url, timeout=timeout, headers={
                             'Connection': 'close'}) for url in urls]
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
