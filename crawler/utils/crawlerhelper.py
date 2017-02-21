#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawlerutils import cleanHTML

def fetchNews(url, encoding='utf-8'):
    r = requests.get(url)
    r.encoding = encoding
    url = r.url
    html = cleanHTML(r.text)
    news = NewsDataProcessor(url, html)

    return news.output()
