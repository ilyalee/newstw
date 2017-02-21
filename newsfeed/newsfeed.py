#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from newsfeed.utils.newsfeedhelper import fetchFeed

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = ''
    if 'url' in request.args:
        url = request.args['url'][0]
    else:
        return json({'newsfeed'})

    filterText = ''
    if 'include' in request.args:
        includeText = request.args['include'][0]

    return json(fetchFeed(url, includeText), ensure_ascii=False)
