#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
#from archiver.utils.archiver_helper import flag
app = Sanic(__name__)


@app.route("/")
async def index(request, methods=['GET']):
    return json(None, ensure_ascii=False)
