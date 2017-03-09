from sanic.response import json
from sanic.views import HTTPMethodView
from newsfeed.utils.newsfeed_helper import fetch_feed
from db.providers.archive_provider import ArchiveProvider

class NewsfeedController(HTTPMethodView):

    ap = ArchiveProvider()

    async def get(self, request, hashid):
        """ show archive by hashid
         Args:
             request (str): contains a str of hashed id.
        """
        blockers = ['id', 'hash']
        item = self.ap.load(hashid, blockers)

        return json(item)

    async def post(self, request):
        """ create new archives for newsfeed from a feed url.
         Args:
             request (str): contains a str of feed url.
        """
        url = request.json.get('url')
        items = fetch_feed(url, full_text=False)
        total = len(items)

        # checking duplicate items by hash
        items = self.ap.find_distinct_items_by("hash", items)
        fetch_feed.full_text = True
        items = fetch_feed.postprocess(items)
        ids = self.ap.save_all(items)
        acceptances = len(ids)
        rejects = total - acceptances

        data = {
            'acceptances': acceptances,
            'rejects': rejects,
            'items': ids,
            'info': '%d successfully created, %d duplicates found.' % (acceptances, rejects)
        }

        return json(data)
