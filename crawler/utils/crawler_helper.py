#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html
from db.utils.db_utils import as_run_pro


def fetch_news(url, encoding='utf-8', timeout=60):
    import requests
    session = requests.session()
    output = {}
    r = session.get(url=url, timeout=timeout)
    r.encoding = encoding
    session.close()
    html = clean_html(r.text)
    return NewsDataProcessor(r.url, html).output()

async def as_fetch_news(url, encoding='utf-8', timeout=60):
    import requests
    resp = await as_run_pro(session.get, url, timeout=timeout)
    resp.encoding = encoding
    session.close()
    html = clean_html(resp.text)
    return await NewsDataProcessor(resp.url, html).as_output()

def fetch_news_all(urls, encoding='utf-8', timeout=60):
    if isinstance(urls, list):
        return fetch_news_all_v2(urls, encoding, timeout)

def fetch_news_all_v2(urls, encoding, timeout):
    import requests
    from concurrent.futures import ProcessPoolExecutor
    from requests_futures.sessions import FuturesSession

    collect = []
    resopones = []
    session = FuturesSession(session=requests.Session(), executor=ProcessPoolExecutor(max_workers=os.cpu_count()))
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

def fetch_news_all_v1(urls, encoding, timeout):
    import grequests, requests

    def _hook(*encoding):
        def hook(resp, **kwargs):
            resp.encoding = encoding
            return resp
        return hook

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

def fetch_news_all_v0(urls, encoding, timeout):
    import requests

    collect = []
    resopones = []
    session = requests.session()
    resopones = [session.get(url=url, timeout=timeout) for url in urls]
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
