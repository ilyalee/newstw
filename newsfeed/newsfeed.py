#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from newsfeed.utils.newsfeedhelper import fetchFeed

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    urls = []
    if 'url' in request.args:
        urls = request.args['url']
    else:
        return json({'newsfeed'})

    includeText = ''
    if 'include' in request.args:
        includeText = request.args['include'][0]

    fulltext = False
    if 'fulltext' in request.args:
        if request.args['fulltext'][0].lower() == 'true':
            fulltext = True
        
    feed = []
    for url in urls:
        feed += fetchFeed(url, includeText, fulltext=fulltext)

    return json(feed, ensure_ascii=False)
