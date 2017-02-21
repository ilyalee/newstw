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
