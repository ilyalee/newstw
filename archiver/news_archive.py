#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1
from sanic.response import html
from archiver.utils.archiver_helper import as_fetch_report, as_fetch_report_count, as_fetch_report_today, as_fetch_report_week, as_fetch_report_today_count, as_fetch_report_week_count
from jinja2 import Environment, PackageLoader, select_autoescape, Markup, escape
from sanic.config import Config
from utils.type_utils import sint
from utils.data_utils import hightlight_keywords
from db.utils.db_utils import reload_keyword


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
    limit = 10
    data['page'] = sint(request.args.get('page', page), page)
    data['limit'] = sint(request.args.get('limit', limit), limit)
    keyword = request.args.get('keyword', None)
    data['keyword'] = keyword
    data['_keyword'] = keyword
    data['category'] = request.args.get('cat', None)
    data['parent'] = request.args.get('parent', None)
    if data['_keyword'] == data['parent']:
        data['parent'] = ""
    data['parent_count'] = await as_fetch_report_count(data['parent'], data['category'])
    if data['parent'] and data['keyword']:
        data['_keyword'] = " ".join({data['_keyword'], data['parent']})
    data['count'] = await as_fetch_report_count(data['_keyword'], data['category'])
    data['items'] = await as_fetch_report(data['page'], data['limit'], data['_keyword'], data['category'])
    (data['_keyword'], _) = reload_keyword(data['_keyword'])
    if data['category']:
        import configparser
        config = configparser.ConfigParser()
        config.read('config/feeds.cfg')
        data['category_zh_tw'] = config.get('zh_tw', data['category'])

    return html(template.render(data=data))


@app.route("/today")
async def index(request, methods=['GET']):
    data = {}
    page = 1
    limit = 10
    data['page'] = sint(request.args.get('page', page), page)
    data['limit'] = sint(request.args.get('limit', limit), limit)
    keyword = request.args.get('keyword', None)
    data['keyword'] = keyword
    data['_keyword'] = keyword
    data['category'] = request.args.get('cat', None)
    data['parent'] = request.args.get('parent', None)
    data['parent_count'] = await as_fetch_report_today_count(data['parent'], data['category'])
    if data['parent'] and data['_keyword']:
        data['_keyword'] = " ".join({data['_keyword'], data['parent']})
    data['count'] = await as_fetch_report_today_count(data['_keyword'], data['category'])
    data['items'] = await as_fetch_report_today(data['page'], data['limit'], data['_keyword'], data['category'])
    (data['_keyword'], _) = reload_keyword(data['_keyword'])
    if data['category']:
        import configparser
        config = configparser.ConfigParser()
        config.read('config/feeds.cfg')
        data['category_zh_tw'] = config.get('zh_tw', data['category'])

    return html(template.render(data=data))


@app.route("/week")
async def index(request, methods=['GET']):
    data = {}
    page = 1
    limit = 10
    data['page'] = sint(request.args.get('page', page), page)
    data['limit'] = sint(request.args.get('limit', limit), limit)
    keyword = request.args.get('keyword', None)
    data['keyword'] = keyword
    data['_keyword'] = keyword
    data['category'] = request.args.get('cat', None)
    data['parent'] = request.args.get('parent', None)
    data['parent_count'] = await as_fetch_report_week_count(data['parent'], data['category'])
    if data['parent'] and data['_keyword']:
        data['_keyword'] = " ".join({data['_keyword'], data['parent']})
    data['count'] = await as_fetch_report_week_count(data['_keyword'], data['category'])
    data['items'] = await as_fetch_report_week(data['page'], data['limit'], data['_keyword'], data['category'])
    (data['_keyword'], _) = reload_keyword(data['_keyword'])
    if data['category']:
        import configparser
        config = configparser.ConfigParser()
        config.read('config/feeds.cfg')
        data['category_zh_tw'] = config.get('zh_tw', data['category'])

    return html(template.render(data=data))
