#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json
from archiver.blueprints import bp_v1
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic.config import Config
import setproctitle
from html import unescape

setproctitle.setproctitle(__name__)

app = Sanic(__name__)
app.static('/static', 'archiver/static')
app.blueprint(bp_v1)

Config.REQUEST_TIMEOUT = 300
env = Environment(
    loader=PackageLoader('archiver', 'templates'),
    autoescape=select_autoescape(['html'])
)
env.filters['unescape'] = unescape
template = env.get_template('index.html')
facebook_template = env.get_template('facebook.html')
stats_template = env.get_template('stats.html')


@app.route('/')
@app.head('/')
async def index(request, methods=['GET']):
    from archiver.controllers.newsfeedlist import as_request_report
    return html(template.render(data=await as_request_report(request, count=True), debug=__debug__))


@app.route('/daily')
@app.head('/daily')
async def index(request, methods=['GET']):
    from archiver.controllers.newsfeedlist import as_request_report
    return html(template.render(data=await as_request_report(request, 'daily', count=True), debug=__debug__))


@app.route("/weekly")
@app.head('/weekly')
async def index(request, methods=['GET']):
    from archiver.controllers.newsfeedlist import as_request_report
    return html(template.render(data=await as_request_report(request, 'weekly', count=True), debug=__debug__))


@app.route('/fb')
@app.head('/fb')
async def index(request, methods=['GET']):
    from archiver.controllers.fbfeedlist import as_request_report
    return html(facebook_template.render(data=await as_request_report(request, count=True), debug=__debug__))


@app.route('/fb/daily')
@app.head('/fb/daily')
async def index(request, methods=['GET']):
    from archiver.controllers.fbfeedlist import as_request_report
    return html(facebook_template.render(data=await as_request_report(request, 'daily', count=True), debug=__debug__))


@app.route("/fb/weekly")
@app.head('/fb/weekly')
async def index(request, methods=['GET']):
    from archiver.controllers.fbfeedlist import as_request_report
    return html(facebook_template.render(data=await as_request_report(request, 'weekly', count=True), debug=__debug__))


@app.route('/stats')
@app.head('/stats')
async def index(request, methods=['GET']):
    import arrow
    from archiver.controllers.newsfeedlist import as_report_count, as_report, as_observer_count, as_observer
    data = {
        'count': await as_report_count(),
        'today': await as_report_count('today'),
        'yesterday': await as_report_count('yesterday'),
        'month': await as_report_count('month'),
        'observer_count': await as_observer_count(),
        'observer_today': await as_observer_count('today'),
        'observer_yesterday': await as_observer_count('yesterday'),
        'observer_month': await as_observer_count('month')
    }

    firstone = await as_report(None, 1, 1)
    observer_firstone = await as_observer(None, 1, 1)
    if firstone:
        data['since'] = arrow.get(firstone[0]['created']).format('YYYY.MM.DD')
    if observer_firstone:
        data['observer_since'] = arrow.get(observer_firstone[0]['created']).format('YYYY.MM.DD')

    return html(stats_template.render(data=data, debug=__debug__))
