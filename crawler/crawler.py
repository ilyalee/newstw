#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from crawler.utils.crawlerhelper import fetchNews

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = ''
    if 'url' in request.args:
        url = request.args['url'][0]
    else:
        return json({'crawler'})

    return json(fetchNews(url), ensure_ascii=False)
