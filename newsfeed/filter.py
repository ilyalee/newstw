#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import requests
import os
import asyncio
import functools
from utils.data_utils import dict_filter, time_corrector, link_corrector, data_cleaner, data_filter, data_inserter, data_updater, data_kv_updater_all, data_hasher
from crawler.utils.crawler_helper import fetch_news_all
from crawler.utils.crawler_utils import detect_news_source
from concurrent.futures import ThreadPoolExecutor

class NewsFeedFilter:

    def __init__(self, url, include_text='', full_text=False):
        self.url = url
        self.full_text = full_text
        self.include_text = include_text

    def _download(self, encoding='utf-8', timeout=30):
        session = requests.Session()
        resp = session.get(self.url, timeout=timeout)
        resp.connection.close()
        resp.encoding = encoding
        items = {}
        rawdata = feedparser.parse(resp.text)
        items = rawdata['entries']
        items = self.postprocess(items)
        return items

    async def _as_download(self, encoding='utf-8', timeout=30):
        executor = ThreadPoolExecutor(os.cpu_count())
        loop = asyncio.get_event_loop()
        session = requests.Session()
        resp = await loop.run_in_executor(executor, functools.partial(session.get, self.url, timeout=timeout))
        resp.connection.close()
        resp.encoding = encoding
        items = {}
        rawdata = feedparser.parse(resp.text)
        items = rawdata['entries']
        items = await self.as_postprocess(items)
        return items

    def _data_prepare(self, items):
        items = data_kv_updater_all("summary", "link", fetch_news_all, self.full_text, items)
        return items

    def _data_filter(self, items):
        keys = ['title', 'published', 'link', 'summary', 'updated', 'full_text']
        items = dict_filter(keys, items)
        items = time_corrector("published", items)
        items = time_corrector("updated", items)
        items = link_corrector("link", items)
        items = data_cleaner("title", items)
        items = data_cleaner("summary", items)
        items = data_filter(self.include_text, ["summary", "title"], items)
        return items

    def _data_produce(self, items):
        items = data_inserter(self.include_text, "keyword", items)
        items = data_updater("source", "link", detect_news_source, True, items)
        items = data_hasher("hash", ["title", "published", "source"], items)
        return items

    def postprocess(self, items):
        items = self._data_prepare(items)
        items = self._data_filter(items)
        return self._data_produce(items)

    async def as_postprocess(self, items):
        loop = asyncio.get_event_loop()
        items = await loop.run_in_executor(None, functools.partial(self._data_prepare, items))
        items = await loop.run_in_executor(None, functools.partial(self._data_filter, items))
        items = await loop.run_in_executor(None, functools.partial(self._data_produce, items))
        return items

    def output(self):
        return self._download()

    async def as_output(self):
        return await self._as_download()
