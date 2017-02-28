#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1

app = Sanic(__name__)
app.blueprint(bp_v1)

@app.route("/")
async def index(request, methods=['GET']):
    return json(['news archiver'], ensure_ascii=False)
