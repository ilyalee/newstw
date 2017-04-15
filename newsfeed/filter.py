#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
import requests
from requests.exceptions import RequestException
import os
import asyncio
from functools import partial
from utils.data_utils import dict_filter, time_corrector, link_corrector, data_cleaner, data_filter, data_inserter, data_updater, data_kv_updater_all_load, data_kv_updater_all_by_remote_items, data_hasher, data_remover
from crawler.utils.crawler_helper import fetch_news_all
from crawler.utils.crawler_utils import detect_news_source
from newsfeed.utils.newsfeed_helper import load_remote_news_date
from utils.async_utils import as_run
import logging
log = logging.getLogger(__name__)
from typing import List
Feeds = List[dict]


class NewsFeedFilter:

    def __init__(self, url, include_text='', full_text=False, connections=None):
        self.url = url
        self.full_text = full_text
        self.include_text = include_text
        self.source = detect_news_source(url)
        self.connections = connections

    def _download(self, encoding='utf-8', timeout=30, limit=5) -> Feeds:
        items = []
        if 'any' == self.source:
            return items
        remedy = 0
        while remedy < limit:
            if remedy > 0:
                log.error(f"[{__name__}] Retry: {self.url}")
            with requests.Session() as session:
                try:
                    resp = session.get(self.url, timeout=timeout)
                    resp.encoding = encoding
                    text = resp.text
                except RequestException as e:
                    remedy = remedy + 1
                    log.error(f"[{__name__}] Failure when trying to fetch { self.url}")
                    log.info(e, exc_info=True)
                else:
                    remedy = 0
                    rawdata = feedparser.parse(resp.text)
                    items = self.postprocess(rawdata['entries'])
                    break
        return items

    async def _as_download(self, encoding='utf-8', timeout=30, limit=5) -> Feeds:
        items = []
        url = self.url
        remedy = 0
        while remedy < limit:
            if remedy > 0:
                log.error(f"[{__name__}] Retry: {url}")
            with requests.Session() as session:
                try:
                    resp = await as_run()(session.get)(url, timeout=timeout)
                    resp.encoding = encoding
                    text = resp.text
                except RequestException as e:
                    remedy = remedy + 1
                    log.error(f"[{__name__}] Failure when trying to fetch {url}")
                    log.info(e, exc_info=True)
                else:
                    remedy = 0
                    rawdata = feedparser.parse(text)
                    items = await self.as_postprocess(rawdata['entries'])
                    break
        return items

    def _data_prepare(self, items):
        items = items[:self.connections]

        keys = ['title', 'published', 'link', 'summary', 'updated', 'full_text']
        items = dict_filter(keys, items)
        items = data_updater("summary", "content", lambda content: content[0][
                             'value'],  all("content" in item for item in items), items)

        items = time_corrector("published", items)
        items = time_corrector("updated", items)
        items = link_corrector("link", items)
        items = data_cleaner("title", items)
        items = data_cleaner("summary", items)

        if not self.full_text:
            if 'supplements' == self.source:
                items = data_updater("source", "link", detect_news_source, True, items)
            else:
                items = data_updater("source", "link", detect_news_source, self.url, items)
        else:
            items = data_updater("source", "link", detect_news_source, True, items)
        items = data_remover("any", "source", items)

        remote_items = data_kv_updater_all_load("link", partial(
            fetch_news_all, source=self.source), self.full_text, items)
        items = data_kv_updater_all_by_remote_items(
            remote_items, "summary", "summary", self.full_text, items)
        items = data_kv_updater_all_by_remote_items(
            remote_items, "published", "published", self.full_text, items)
        items = data_kv_updater_all_by_remote_items(
            remote_items, "source", "source", self.full_text, items)
        return items

    def _data_filter(self, items):
        items = data_filter(self.include_text, ["summary", "title"], items)
        return items

    def _data_produce(self, items):
        items = data_inserter(self.include_text, "keyword", items)
        if (__debug__) and 0 == len(items) and 'any' == self.source:
            print("please debug this source: {} | {}".format(
                self.url, detect_news_source(self.url)))
        items = data_hasher("hash", ["title", "published", "source"], items)
        return items

    def postprocess(self, items):
        items = self._data_prepare(items)
        items = self._data_filter(items)
        return self._data_produce(items)

    async def as_postprocess(self, items):
        items = await as_run(mode='process')(self._data_prepare)(items)
        items = await as_run(mode='process')(self._data_filter)(items)
        items = await as_run(mode='process')(self._data_produce)(items)
        return items

    def output(self):
        return self._download()

    async def as_output(self):
        return await self._as_download()
