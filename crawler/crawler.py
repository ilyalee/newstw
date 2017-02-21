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
        return json({'newstw'})

    return json(fetchNews(url), ensure_ascii=False)


app.run(host="0.0.0.0", port=9527, debug=True)
