#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1
from sanic.response import html
from db.providers.archive_provider import ArchiveProvider
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic.config import Config

Config.REQUEST_TIMEOUT = 300
env = Environment(
    loader=PackageLoader('archiver', 'templates'),
    autoescape=select_autoescape(['html'])
)

app = Sanic(__name__)
app.blueprint(bp_v1)

template = env.get_template('index.html')
ap = ArchiveProvider()

@app.route("/")
async def index(request, methods=['GET']):
    data = {}
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 5)
    #TODO: check numeric type and check numbers are positive
    data['items'] = await ap.as_load_report_by_page(int(page), int(limit))
    return html(template.render(data=data))
