#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from fbfeed.utils.fbfeed_helper import flag
from fbfeed.utils.fbfeed_helper import fetch_feed

app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    fbid = request.args.get("fbid")
    if not fbid:
        return json({'fbfeed'})
    num = request.args.get("num", 1)
    include_text = request.args.get("include")
    search = flag(request.args.get("search", False))
    feed = fetch_feed(fbid, num, include_text, search)

    return json(feed, ensure_ascii=False)
