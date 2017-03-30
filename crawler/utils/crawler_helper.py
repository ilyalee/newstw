#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawler_utils import clean_html, detect_news_source
from utils.async_utils import as_run
import requests
from requests.exceptions import RequestException
import logging
log = logging.getLogger(__name__)


def fetch_news(url, encoding='utf-8', timeout=60):
    with requests.session() as session:
        try:
            resp = session.get(url=url, timeout=timeout)
            resp.encoding = encoding
            text = resp.text
        except RequestException as e:
            log.error(f"[{__name__}] Failure when trying to fetch {url}")
            log.info(e, exc_info=True)
        else:
            html = clean_html(text)
            return NewsDataProcessor(resp.url, html).output()

async def as_fetch_news(url, encoding='utf-8', timeout=60):
    with requests.session() as session:
        try:
            resp = await as_run()(session.get)(url, timeout=timeout)
            resp.encoding = encoding
            text = resp.text
        except RequestException as e:
            log.error(f"[{__name__}] Failure when trying to fetch {url}")
            log.info(e, exc_info=True)
        else:
            html = clean_html(resp.text)
            return await NewsDataProcessor(resp.url, html).as_output()


def fetch_news_all(urls, encoding='utf-8', timeout=60, limit=5, remedy=False, total_connection=100, source=None):
    from concurrent.futures import ThreadPoolExecutor
    from requests_futures.sessions import FuturesSession
    import threading
    sem = threading.Semaphore(limit)
    collect = []
    resopones = []
    with FuturesSession(session=requests.Session(),
                        executor=ThreadPoolExecutor(max_workers=os.cpu_count())) as session:
        connection = 0
        failed_urls = []
        futures = ((url, session.get(url, timeout=timeout)) for url in urls)
        for url, future in futures:
            connection = connection + 1
            if connection > total_connection:
                break
            target_source = None
            if not source:
                source = detect_news_source(url)
            else:
                url_source = detect_news_source(url)
                if 'supplements' == source:
                    target_source = url_source
                elif url_source == source:
                    target_source = source
                elif 'youtube' == url_source:
                    target_source = source
                else:
                    target_source = 'any'
            if __debug__:
                print(f"[{target_source}:{connection}] ({url})")
            if remedy:
                log.error(f"[{__name__}] Retry: {url}")
            try:
                with sem:
                    resopones.append((target_source, future.result()))
            except requests.exceptions.RequestException as e:
                failed_urls.append(url)
                log.error(f"[{__name__}] Failure when trying to fetch {url}")
                log.info(e, exc_info=True)
                continue
        for (target_source, resp) in resopones:
            resp.encoding = encoding
            html = clean_html(resp.text)
            news = NewsDataProcessor(resp.url, html, target_source)
            output = news.output()
            collect.append(output)
    if failed_urls:
        return collect + fetch_news_all(failed_urls, encoding, timeout, limit, True, total_connection, source)
    else:
        return collect
