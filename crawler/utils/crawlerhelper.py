#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from crawler.newsprocessor import NewsDataProcessor
from crawler.utils.crawlerutils import cleanHTML

def fetchNews(url, encoding='utf-8'):
    output = {}
    r = requests.get(url)
    r.encoding = encoding
    r.close()
    html = cleanHTML(r.text)
    news = NewsDataProcessor(r.url, html)
    output = news.output()
    
    return output
