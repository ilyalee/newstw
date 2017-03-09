#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from crawler.utils.crawler_utils import load_context, load_skips, load_trimtext, detect_news_source
from utils.data_utils import normalize_news, del_key, trim_data_val, localize_datetime, normalize_link
import asyncio
import functools
import os
from concurrent.futures import ThreadPoolExecutor


class NewsDataProcessor:

    def __init__(self, url, html):
        self.data = {}
        self.soup = BeautifulSoup(html, "html.parser")
        self.url = normalize_link(url)
        self.html = html
        self.source = detect_news_source(self.url)
        self.context = load_context(self.source)
        self.trimtext = load_trimtext(self.source)

    def output(self):
        self._process(self.html)
        self.data['pass'] = self.data.get("pass", True)
        return self.data

    async def as_output(self):
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(os.cpu_count())
        await loop.run_in_executor(executor, functools.partial(self._process, self.html))
        self.data['pass'] = self.data.get("pass", True)
        return self.data

    def _process(self, html):
        self.data['link'] = self.url
        self.data['from'] = self.source
        if self.source == 'any':
            self.data['pass'] = False

        self._news_processor(html)
        self._time_corrector()
        del_key("_rawtime", (not __debug__), self.data)

        for text in self.trimtext:
            trim_data_val("summary", text, self.data)

    def _soup_func(self, name, path):
        return {"select": self._soup_select, "find_all": self._soup_find_all, "attrs": self._soup_attrs}.get(name)(path)

    def _soup_attrs(self, path):
        for key, value in path.items():
            return self.soup.find(key).attrs[value]

    def _soup_select(self, path):
        if isinstance(path, list):
            for p in path:
                target = self.soup.select(p)
                if len(target) > 0:
                    break
        else:
            target = self.soup.select(path)
        return target

    def _soup_find_all(self, path):
        return self.soup.find_all(path)

    def _soup(self, skips):
        for skip in skips:
            for tag in self.soup(skip):
                tag.decompose()

    def _news_processor(self, html):
        skips = load_skips(self.source)
        self._soup(skips)
        for c in (context for context in self.context if 'save' in context):
            c['soup'] = c.get("soup", "select")
            text = normalize_news(self._context_to_text(c))
            self.data[c['save']] = text
            if not text:
                self.data['pass'] = False

    def _time_corrector(self):
        for c in (c for c in self.context if '_rawtime' in self.data):
            c['tzinfo'] = c.get("tzinfo", "")
            c['format'] = c.get("format", [])
            self.data['published'] = localize_datetime(
                self.data['_rawtime'], c['format'], c['tzinfo'], self.data)
            if self.data['published'] == '':
                self.data['pass'] = False

    def _context_to_text(self, context):
        text = ''
        if context['ind'] >= 0:
            try:
                context.get("path", "")
                res = self._soup_func(context['soup'], context['path'])
                if isinstance(res, str):
                    text = res
                elif isinstance(res, list):
                    text = res[context['ind']].text
            except IndexError as err:
                self.data['pass'] = False
                if __debug__:
                    self.data['debug'] = err
        else:
            tags = self._soup_func(context['soup'], context['path'])
            text = ''.join([tag.text for tag in tags])

        return text
