#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def cleanHTML(html):
    # remove all whitespaces
    pat = re.compile(r"(^[\s]+)|([\s]+$)", re.MULTILINE)
    html = re.sub(pat, "", html)
    html = re.sub(r"[\s]+<", "<", html)
    html = re.sub(r">[\s]+", ">", html)
    # remove all newlines
    html = re.sub(r"\n", "", html)

    #remove all scripts
    pat = re.compile(r"<(script)[\s\S]+?/script>", re.MULTILINE)
    html = re.sub(pat, "", html)

    #remove all styles
    pat = re.compile(r"<style[\s\S]+?/style>", re.MULTILINE)
    html = re.sub(pat, "", html)

    html = re.sub(r"\u200b", "", html)

    return html

################################################################################
def _soupFunc(soup, name, path):
    return {"select": _soupSelect, "findAll": _soupFindAll, "attrs": _soupAttrs}.get(name)(soup, path)

def _soupAttrs(soup, path):
    for k, v in path.items():
        return soup.find(k).attrs[v]

def _soupSelect(soup, path):
    if isinstance(path, list):
        for p in path:
            target = soup.select(p)
            if len(target) > 0:
                break
    else:
        target = soup.select(path)
    return target

def _soupFindAll(soup, path):
    return soup.find_all(path)

def _soup(html, skips):
    soup = BeautifulSoup(html, "html.parser")
    if skips:
        for tag in soup(skips):
            tag.decompose()
    return soup

def detectNewsSource(url):
    any_in = lambda a, b: any(i in b for i in a)

    from crawler.web_shape_var import source, source_default

    target = source_default

    for t, urls in source.items():
        if any_in(urls, url):
            target = t
            break
    return target

def loadContext(source):
    from crawler.web_shape_var import context

    if source in context:
        return context[source]
    else:
        return context['any']

def loadSkips(source):
    from crawler.web_shape_var import skip

    if source in skip:
        return skip[source]
    else:
        return []

def loadTrimtext(source):
    from crawler.web_shape_var import trimtext

    if source in trimtext:
        return trimtext[source]
    else:
        return []

def fetchNews(url):
    return _fetchNews(url)

################################################################################
import requests
from bs4 import BeautifulSoup
import unicodedata
import arrow

def normalize(text):
    return unicodedata.normalize("NFKD", text)

def _fetchNews(url):
    r = requests.get(url)
    url = r.url
    source = detectNewsSource(url)
    context = loadContext(source)
    skips = loadSkips(source)
    trimtext = loadTrimtext(source)

    r.encoding = "utf-8"
    rawtext = r.text
    html = cleanHTML(rawtext)
    soup = _soup(html, skips)

    data = {}
    for c in context:
        if 'save' not in c:
            continue
        if 'soup' not in c or not c['soup']:
            c['soup'] = 'select'

        text = ''
        if c['ind'] >= 0:
            try:
                if not 'path' in c:
                    c['path'] = ''
                res = _soupFunc(soup, c['soup'], c['path'])
                if isinstance(res, str):
                    text = res
                else:
                    text = res[c['ind']].text

            except IndexError as err:
                if __debug__:
                    data['debug'] = err
        else:
            tags = _soupFunc(soup, c['soup'], c['path'])
            text = ''.join([tag.text for tag in tags])
        data[c['save']] = normalize(text)

    for c in context:
        if 'tzinfo' not in c:
            continue
        if data['_rawtime']:
            try:
                if 'format' in c:
                    data['pubdate'] = arrow.get(data['_rawtime'], c['format']).replace(tzinfo=c['tzinfo']).format()
                else:
                    data['pubdate'] = arrow.get(data['_rawtime']).replace(tzinfo=c['tzinfo']).format()
            except arrow.parser.ParserError as err:
                if __debug__:
                    data['debug'] = err

    delKey("_rawtime", (not __debug__), data)

    data['summary'] = trimDataVal("summary", trimtext, data)
    data['link'] = url
    data['from'] = source

    return data
################################################################################

def trimDataVal(key, trimtext, data):
    if trimtext and key in data:
        for t in trimtext:
            data[key] = re.sub(u'%s$' % t, '', data[key])
    return data[key]

def delKey(key, ok, data):
    if ok:
        data.pop(key, None)
