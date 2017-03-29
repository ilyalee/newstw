#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from fbfeed.utils.fbfeed_helper import flag, as_fetch_feed
import setproctitle

setproctitle.setproctitle(__name__)
app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    fbid = request.args.get("fbid")
    if not fbid:
        return json({'fbfeed'})
    num = request.args.get("num", 1)
    include_text = request.args.get("include")
    search = flag(request.args.get("search", False))
    feed = await as_fetch_feed(fbid, num, include_text, search)

    return json(feed, ensure_ascii=False)
