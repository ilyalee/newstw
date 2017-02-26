from sanic.response import json
from sanic.views import HTTPMethodView
from newsfeed.utils.newsfeed_helper import fetch_feed
from db.providers.archive_provider import ArchiveProvider as AP

class NewsfeedController(HTTPMethodView):

    async def post(self, request):
        """ create new archives for newsfeed from a feed url.
         Args:
             request (str): contains a str of feed url.
        """
        url = request.json.get('url')
        items = fetch_feed(url, full_text=False)
        hashs = [item['hash'] for item in items]
        total = len(items)

        # checking duplicate items by hash
        items = AP.find_distinct_items_by_hashs(hashs, items)
        # checking duplicate items by IntegrityError
        acceptances = AP.save_all(items)
        rejects = total - acceptances

        data = {
            'acceptances': acceptances,
            'rejects': rejects,
            'items': items,
            'info': '%d successfully created, %d duplicates found.' % (acceptances, rejects)
        }

        return json(data)
