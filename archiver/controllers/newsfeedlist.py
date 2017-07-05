from sanic.response import json
from sanic.views import HTTPMethodView
from archiver.utils.archiver_helper import aph
from archiver.utils.observer_stats_helper import osh
from utils.type_utils import sint
from utils.data_utils import data_updater, hightlight_keywords, dict_cleaner
from functools import partial
from db.utils.db_utils import reload_keyword
from utils.config_utils import load_lang

async def as_request_report(request, time='any', hightlight=True, count=False):
    data = {}
    page = 1
    limit = 10
    data['page'] = sint(request.args.get('page', page), page)
    data['limit'] = sint(request.args.get('limit', limit), limit)
    data['category'] = request.args.get('cat', None)

    if data['category']:
        data['category_zh_tw'] = load_lang('zh_tw', data['category'])

    keyword = request.args.get('keyword', None)
    data['keyword'] = keyword
    data['_keyword'] = keyword

    data['items'] = await as_report(time, data['page'], data['limit'], data['_keyword'], data['category'])

    data['parent'] = request.args.get('parent', None)
    if data['parent'] and data['_keyword']:
        data['_keyword'] = " ".join({data['_keyword'], data['parent']})

    if count:
        data['count'] = await as_report_count(time, data['_keyword'], data['category'])
        data['parent_count'] = await as_report_count(time, data['parent'], data['category'])

    if hightlight and data['keyword']:
        data['items'] = data_updater("title", "title", partial(
            hightlight_keywords, keywords=data['keyword']), True, data['items'])
        data['items'] = data_updater("summary", "summary", partial(
            hightlight_keywords, keywords=data['keyword']), True, data['items'])

    if data['keyword']:
        (data['_keyword'], _) = reload_keyword(data['_keyword'])
    return data

async def as_report(time=None, page=None, limit=None, keywords=None, category=None):
    funcs = {
        'daily': aph.as_fetch_report_daily,
        'weekly': aph.as_fetch_report_weekly,
        'all': aph.as_fetch_report
    }

    return await funcs.get(time, aph.as_fetch_report)(page, limit, keywords, category)

async def as_report_count(time=None, keywords=None, category=None):
    funcs = {
        'daily': aph.as_fetch_report_daily_count,
        'weekly': aph.as_fetch_report_weekly_count,
        'today': aph.as_fetch_report_today_count,
        'month': aph.as_fetch_report_month_count,
        'yesterday': aph.as_fetch_report_yesterday_count,
        'all': aph.as_fetch_report_count
    }
    return await funcs.get(time, aph.as_fetch_report_count)(keywords, category)


async def as_observer(time=None, page=None, limit=None):
    funcs = {
        'all': osh.as_fetch_observer
    }

    return await funcs.get(time, osh.as_fetch_observer)(page, limit)

async def as_observer_count(time=None):
    funcs = {
        'today': osh.as_fetch_observer_today_count,
        'month': osh.as_fetch_observer_month_count,
        'yesterday': osh.as_fetch_observer_yesterday_count,
        'all': osh.as_fetch_observer_count
    }
    return await funcs.get(time, osh.as_fetch_observer_count)()


class NewsfeedListController(HTTPMethodView):
    async def get(self, request):
        """
        fetch a list of archives by paging
        """
        time = request.args.get('time', 'any')
        hightlight = request.args.get('hightlight', True)
        return json(await as_request_report(request, time, hightlight), ensure_ascii=False)
