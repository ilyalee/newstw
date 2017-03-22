#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1
from sanic.response import html
from archiver.utils.archiver_helper import as_fetch_report
from jinja2 import Environment, PackageLoader, select_autoescape, Markup, escape
from sanic.config import Config
from utils.type_utils import sint
from utils.data_utils import keyword_builder, hightlight_keywords

Config.REQUEST_TIMEOUT = 300
env = Environment(
    loader=PackageLoader('archiver', 'templates'),
    autoescape=select_autoescape(['html'])
)


env.filters['hightlight_keywords'] = hightlight_keywords

app = Sanic(__name__)
app.blueprint(bp_v1)

template = env.get_template('index.html')


@app.route("/")
async def index(request, methods=['GET']):
    data = {}
    page = 1
    limit = 5
    page = sint(request.args.get('page', page), page)
    limit = sint(request.args.get('limit', limit), limit)
    keyword = request.args.get('keyword', None)
    category = request.args.get('cat', None)

    data['items'] = await as_fetch_report(page, limit, keyword, category)
    data['keywords'] = keyword_builder(keyword)
    return html(template.render(data=data))
