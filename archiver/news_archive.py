#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic.config import Config
from archiver.controllers.newsfeedlist import as_request_report
import setproctitle

setproctitle.setproctitle(__name__)

app = Sanic(__name__)
app.static('/static', 'archiver/static')
app.blueprint(bp_v1)

Config.REQUEST_TIMEOUT = 300
env = Environment(
    loader=PackageLoader('archiver', 'templates'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('index.html')


@app.route('/')
@app.head('/')
async def index(request, methods=['GET']):
    return html(template.render(data=await as_request_report(request), debug=__debug__))


@app.route('/daily')
@app.head('/daily')
async def index(request, methods=['GET']):
    return html(template.render(data=await as_request_report(request, 'daily'), debug=__debug__))


@app.route("/weekly")
@app.head('/weekly')
async def index(request, methods=['GET']):
    return html(template.render(data=await as_request_report(request, 'weekly'), debug=__debug__))
