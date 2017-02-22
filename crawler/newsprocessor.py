#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from crawler.utils.crawlerutils import loadContext, loadSkips, loadTrimtext, detectNewsSource
from crawler.utils.datautils import normalizeNews, delKey, trimDataVal, fixDatetime

class NewsDataProcessor:
    def __init__(self, url, html):
        self.data = {}
        self.soup = BeautifulSoup(html, "html.parser")
        self.url = url
        self.html = html
        self.source = detectNewsSource(self.url)
        self.context = loadContext(self.source)
        self.trimtext = loadTrimtext(self.source)

    def output(self):
        self._process(self.html)
        self.data['pass'] = self.data.get("pass", True)
        return self.data

    def _process(self, html):
        self.data['link'] = self.url
        self.data['from'] = self.source
        if self.source == 'any':
            self.data['pass'] = False

        self._news_processor(html)
        self._time_corrector()
        delKey("_rawtime", (not __debug__), self.data)

        for text in self.trimtext:
            trimDataVal("summary", text, self.data)

    def _soupFunc(self, name, path):
        return {"select": self._soupSelect, "findAll": self._soupFindAll, "attrs": self._soupAttrs}.get(name)(path)

    def _soupAttrs(self, path):
        for k, v in path.items():
            return self.soup.find(k).attrs[v]

    def _soupSelect(self, path):
        if isinstance(path, list):
            for p in path:
                target = self.soup.select(p)
                if len(target) > 0:
                    break
        else:
            target = self.soup.select(path)
        return target

    def _soupFindAll(self, path):
        return self.soup.find_all(path)

    def _soup(self, skips):
        for skip in skips:
            for tag in self.soup(skip):
                tag.decompose()

    def _news_processor(self, html):
        skips = loadSkips(self.source)
        self._soup(skips)
        for c in (context for context in self.context if 'save' in context):
            c['soup'] = c.get("soup", "select")
            text = normalizeNews(self._context_to_text(c))
            self.data[c['save']] = text
            if not text:
                self.data['pass'] = False

    def _time_corrector(self):
        for c in (c for c in self.context if '_rawtime' in self.data):
            c['tzinfo'] = c.get("tzinfo", "")
            c['format'] = c.get("format", [])
            self.data['published'] = fixDatetime(self.data['_rawtime'], c['format'], c['tzinfo'], self.data)
            if self.data['published'] == '':
                self.data['pass'] = False

    def _context_to_text(self, context):
        text = ''
        if context['ind'] >= 0:
            try:
                context.get("path", "")
                res = self._soupFunc(context['soup'], context['path'])
                if isinstance(res, str):
                    text = res
                else:
                    text = res[context['ind']].text

            except IndexError as err:
                self.data['pass'] = False
                if __debug__: self.data['debug'] = err
        else:
            tags = self._soupFunc(context['soup'], context['path'])
            text = ''.join([tag.text for tag in tags])

        return text
