#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html
from utils.async_utils import as_run
import requests


def fetch_news(url, encoding='utf-8', timeout=60):
    with requests.session() as session:
        r = session.get(url=url, timeout=timeout)
        r.encoding = encoding
        html = clean_html(r.text)
        return NewsDataProcessor(r.url, html).output()

async def as_fetch_news(url, encoding='utf-8', timeout=60):
    with requests.session() as session:
        resp = await as_run()(session.get)(url, timeout=timeout)
        resp.encoding = encoding
        html = clean_html(resp.text)
        return await NewsDataProcessor(resp.url, html).as_output()


def fetch_news_all(urls, encoding='utf-8', timeout=60, limit=5):
    if isinstance(urls, list):
        return fetch_news_all_v3(urls, encoding, timeout, limit)


def fetch_news_all_v2(urls, encoding, timeout=60):
    from concurrent.futures import ThreadPoolExecutor
    from requests_futures.sessions import FuturesSession

    collect = []
    resopones = []
    session = FuturesSession(session=requests.Session(),
                             executor=ThreadPoolExecutor(max_workers=os.cpu_count()))
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


def fetch_news_all_v3(urls, encoding, timeout=60, limit=5):
    from concurrent.futures import ThreadPoolExecutor
    from requests_futures.sessions import FuturesSession
    import threading
    sem = threading.Semaphore(limit)
    collect = []
    resopones = []
    with FuturesSession(session=requests.Session(),
                        executor=ThreadPoolExecutor(max_workers=os.cpu_count())) as session:
        futures = [(url, session.get(url, timeout=timeout)) for url in urls]
        for url, future in futures:
            try:
                with sem:
                    resopones.append(future.result())
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as err:
                raise ConnectionError('url: {}'.format(url))

        for resp in resopones:
            resp.encoding = encoding
            html = clean_html(resp.text)
            news = NewsDataProcessor(resp.url, html)
            output = news.output()
            collect.append(output)
    return collect


def fetch_news_all_v1(urls, encoding, timeout=60):
    import grequests

    def _hook(*encoding):
        def hook(resp, **kwargs):
            resp.encoding = encoding
            return resp
        return hook

    collect = []
    resopones = []
    session = requests.session()
    rs = (grequests.get(url, session=session, timeout=timeout) for url in urls)
    resopones = grequests.map(rs, size=len(urls), exception_handler=exception_handler)
    for resp in resopones:
        html = clean_html(resp.text)
        news = NewsDataProcessor(resp.url, html)
        output = news.output()
        collect.append(output)
    session.close()

    return collect


def fetch_news_all_v0(urls, encoding, timeout=60):
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
