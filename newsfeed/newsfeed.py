#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from newsfeed.utils.newsfeed_helper import flag
from newsfeed.filter import NewsFeedFilter

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    url = request.args.get('url')
    if not 'url':
        return json({'newsfeed'})

    include_text = request.args.get('include')
    full_text = flag(request.args.get('fulltext', False))
    feed = NewsFeedFilter(url, include_text, full_text).output()
    return json(feed, ensure_ascii=False)
