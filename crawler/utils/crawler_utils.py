#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def clean_html(html):
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

def detect_news_source(url):
    any_in = lambda a, b: any(i in b for i in a)

    from crawler.web_shape_var import source, source_default

    target = source_default

    for t, urls in source.items():
        if any_in(urls, url):
            target = t
            break
    return target

def load_context(source):
    from crawler.web_shape_var import context
    return context.get(source, context.get("any", []))

def load_skips(source):
    from crawler.web_shape_var import skip
    return skip.get(source, [])

def load_trimtext(source):
    from crawler.web_shape_var import trimtext
    return trimtext.get(source, [])
