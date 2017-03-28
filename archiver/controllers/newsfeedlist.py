from sanic.response import json
from sanic.views import HTTPMethodView
from archiver.utils.archiver_helper import as_fetch_report
from utils.type_utils import sint


class NewsfeedListController(HTTPMethodView):
    async def get(self, request):
        """
        fetch a list of archives by paging
        """
        page = sint(request.args.get('page', 1), 1)
        limit = sint(request.args.get('limit', 10), 10)
        keywords = request.args.get('keyword', None)
        category = request.args.get('cat', None)
        items = await as_fetch_report(page, limit, keywords, category)
        return json(items, ensure_ascii=False)
