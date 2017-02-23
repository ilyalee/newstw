#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from fbfeed.utils.fbfeedhelper import flag
from fbfeed.utils.fbfeedhelper import fetchFeed

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    fbid = request.args.get("fbid")
    if not fbid:
        return json({'fbfeed'})
    num = request.args.get("num", 1)
    includeText = request.args.get("include")
    search = flag(request.args.get("search", False))
    feed = fetchFeed(fbid, num, includeText, search)

    return json(feed, ensure_ascii=False)
