#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import requests
import os
import asyncio
import functools
from utils.data_utils import dict_filter, time_corrector, link_corrector, data_cleaner, data_filter, data_inserter, data_updater, data_kv_updater_all_load, data_kv_updater_all_by_remote_items, data_hasher, data_remover
from crawler.utils.crawler_helper import fetch_news_all
from crawler.utils.crawler_utils import detect_news_source
from newsfeed.utils.newsfeed_helper import load_remote_news_date
from utils.async_utils import as_run, as_run_pro


class NewsFeedFilter:

    def __init__(self, url, include_text='', full_text=False):
        self.url = url
        self.full_text = full_text
        self.include_text = include_text

    def _download(self, encoding='utf-8', timeout=30):
        session = requests.Session()
        resp = session.get(self.url, timeout=timeout)
        session.close()
        resp.encoding = encoding
        rawdata = feedparser.parse(resp.text)
        items = self.postprocess(rawdata['entries'])
        return items

    async def _as_download(self, encoding='utf-8', timeout=30):
        session = requests.Session()
        resp = await as_run(session.get, self.url, timeout=timeout)
        session.close()
        resp.encoding = encoding
        rawdata = feedparser.parse(resp.text)
        items = await self.as_postprocess(rawdata['entries'])
        return items

    def _data_prepare(self, items):
        keys = ['title', 'published', 'link', 'summary', 'updated', 'full_text']
        items = dict_filter(keys, items)
        items = data_updater("summary", "content", lambda content: content[0][
                             'value'],  all("content" in item for item in items), items)

        items = time_corrector("published", items)
        items = time_corrector("updated", items)
        items = link_corrector("link", items)
        items = data_cleaner("title", items)
        items = data_cleaner("summary", items)

        remote_items = data_kv_updater_all_load("link", fetch_news_all, self.full_text, items)
        items = data_kv_updater_all_by_remote_items(
            remote_items, "summary", "link", fetch_news_all, self.full_text, items)
        items = data_kv_updater_all_by_remote_items(
            remote_items, "published", "published", load_remote_news_date, self.full_text, items)
        return items

    def _data_filter(self, items):
        items = data_filter(self.include_text, ["summary", "title"], items)
        return items

    def _data_produce(self, items):
        items = data_inserter(self.include_text, "keyword", items)
        items = data_updater("source", "link", detect_news_source, self.url, items)
        items = data_remover("any", "source", items)
        if (__debug__) and 0 == len(items):
            print("please debug this source: {} | {}".format(
                self.url, detect_news_source(self.url)))
        items = data_hasher("hash", ["title", "published", "source"], items)
        return items

    def postprocess(self, items):
        items = self._data_prepare(items)
        items = self._data_filter(items)
        return self._data_produce(items)

    async def as_postprocess(self, items):
        items = await as_run(self._data_prepare, items)
        items = await as_run(self._data_filter, items)
        items = await as_run(self._data_produce, items)
        return items

    def output(self):
        return self._download()

    async def as_output(self):
        return await self._as_download()
