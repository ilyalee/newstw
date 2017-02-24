#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

from archiver.controllers.newsfeed import NewsfeedController
app.add_route(NewsfeedController().as_view(), 'api/v1/news/archive')

@app.route("/")
async def index(request, methods=['GET']):
    return json(['news archiver'], ensure_ascii=False)
