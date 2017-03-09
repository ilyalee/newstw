#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from crawler.utils.crawler_helper import as_fetch_news

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = request.args.get('url')
    if not url:
        return json({'crawler'})
    obj = await as_fetch_news(url)
    return json(obj, ensure_ascii=False)
