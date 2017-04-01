from sanic.response import json
from sanic.views import HTTPMethodView
from archiver.utils.archiver_helper import as_fetch_report, as_fetch_report_count, as_fetch_report_daily, as_fetch_report_weekly, as_fetch_report_daily_count, as_fetch_report_weekly_count
from utils.type_utils import sint
from utils.data_utils import data_updater, hightlight_keywords
from functools import partial
from db.utils.db_utils import reload_keyword

async def as_request_report(request, time='any', hightlight=True):
    data = {}
    page = 1
    limit = 10
    data['page'] = sint(request.args.get('page', page), page)
    data['limit'] = sint(request.args.get('limit', limit), limit)
    data['category'] = request.args.get('cat', None)

    keyword = request.args.get('keyword', None)
    data['keyword'] = keyword
    data['_keyword'] = keyword

    data['items'] = await as_report(time, data['page'], data['limit'], data['_keyword'], data['category'])
    data['count'] = await as_report_count(time, data['_keyword'], data['category'])

    data['parent'] = request.args.get('parent', None)
    data['parent_count'] = await as_report_count(time, data['parent'], data['category'])
    if data['parent'] and data['_keyword']:
        data['_keyword'] = " ".join({data['_keyword'], data['parent']})

    if data['category']:
        import configparser
        config = configparser.ConfigParser()
        config.read('config/feeds.cfg')
        data['category_zh_tw'] = config.get('zh_tw', data['category'])

    if hightlight and data['keyword']:
        data['items'] = data_updater("title", "title", partial(
            hightlight_keywords, keywords=data['keyword']), True, data['items'])
        data['items'] = data_updater("summary", "summary", partial(
            hightlight_keywords, keywords=data['keyword']), True, data['items'])

    if data['keyword']:
        (data['_keyword'], _) = reload_keyword(data['_keyword'])
    return data

async def as_report(time, page, limit, keywords, category):
    funcs = {
        'daily': as_fetch_report_daily,
        'weekly': as_fetch_report_weekly
    }
    return await funcs.get(time, as_fetch_report)(page, limit, keywords, category)

async def as_report_count(time, keywords, category):
    funcs = {
        'daily': as_fetch_report_daily_count,
        'weekly': as_fetch_report_weekly_count
    }
    return await funcs.get(time, as_fetch_report_count)(keywords, category)


class NewsfeedListController(HTTPMethodView):
    async def get(self, request):
        """
        fetch a list of archives by paging
        """
        time = request.args.get('time', 'any')
        hightlight = request.args.get('hightlight', True)
        return json(await as_request_report(request, time, hightlight), ensure_ascii=False)
