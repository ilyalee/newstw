from sanic.response import json
from sanic.views import HTTPMethodView
from db.providers.archive_provider import ArchiveProvider
from newsfeed.filter import NewsFeedFilter

class NewsfeedController(HTTPMethodView):

    ap = ArchiveProvider()

    async def get(self, request, hashid):
        """ show archive by hashid
         Args:
             request (str): contains a str of hashed id.
        """
        item = await self.ap.as_load(hashid, ['id', 'hash'])

        return json(item, ensure_ascii=False)

    async def post(self, request):
        """ create new archives for newsfeed from a feed url.
         Args:
             request (str): [url, include_text]
        """
        url = request.json.get('url')
        include_text = request.json.get('include')
        feed = NewsFeedFilter(url, include_text, full_text=True)
        items = await feed.as_output()
        total = len(items)

        # checking duplicate items by hash
        items = await self.ap.as_find_distinct_items_by("hash", items)
        #feed.full_text = True
        #items = feed.postprocess(items)
        ids = await self.ap.as_save_all(items)
        acceptances = len(ids)
        rejects = total - acceptances

        data = {
            'url': url,
            'acceptances': acceptances,
            'rejects': rejects,
            'items': ids,
            'info': '%d successfully created, %d duplicates found.' % (acceptances, rejects)
        }

        return json(data, ensure_ascii=False)
