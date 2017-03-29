from sanic.response import json
from sanic.views import HTTPMethodView
from archiver.utils.archiver_helper import as_fetch_report, as_fetch_report_today, as_fetch_report_week
from utils.type_utils import sint
from utils.data_utils import data_updater, hightlight_keywords
from functools import partial


async def as_report(time, page, limit, keywords, category):
    funcs = {
        'today': as_fetch_report_today,
        'week': as_fetch_report_week
    }
    return await funcs.get(time, as_fetch_report)(page, limit, keywords, category)


class NewsfeedListController(HTTPMethodView):
    async def get(self, request):
        """
        fetch a list of archives by paging
        """
        time = request.args.get('time', None)

        page = 1
        limit = 10
        page = sint(request.args.get('page', page), page)
        limit = sint(request.args.get('limit', limit), limit)
        keywords = request.args.get('keyword', None)
        category = request.args.get('cat', None)

        items = await as_report(time, page, limit, keywords, category)
        items = data_updater("title", "title", partial(
            hightlight_keywords, keywords=keywords), True, items)
        items = data_updater("summary", "summary", partial(
            hightlight_keywords, keywords=keywords), True, items)

        return json(items, ensure_ascii=False)
