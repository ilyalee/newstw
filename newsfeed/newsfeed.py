#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from newsfeed.utils.newsfeedhelper import flag
from newsfeed.utils.newsfeedhelper import fetchFeed

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = request.args.get('url')
    if not 'url':
        return json({'newsfeed'})

    includeText = request.args.get('include')
    fulltext = flag(request.args.get('fulltext', False))
    feed = fetchFeed(url, includeText, fulltext=fulltext)

    return json(feed, ensure_ascii=False)
