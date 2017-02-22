#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from crawler.utils.crawlerhelper import fetchNews

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = request.args.get('url')
    if not url:
        return json({'crawler'})

    obj = fetchNews(url)
    return json(obj, ensure_ascii=False)
