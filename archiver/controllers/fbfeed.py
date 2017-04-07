from sanic.response import json
from sanic.views import HTTPMethodView
from utils.data_utils import dict_cleaner, dict_blocker
from utils.type_utils import sint
from fbfeed.utils.fbfeed_helper import as_fetch_feed


class FbfeedController(HTTPMethodView):

    from db.providers import FacebookArchiveProvider
    ap = FacebookArchiveProvider()

    async def get(self, request, hashid):
        """ show archive by hashid
         Args:
             hashed: contains a str of hashed id.
        """
        item = await self.ap.as_load(hashid, ['id', 'hash'])

        return json(item, ensure_ascii=False)

    async def post(self, request):
        """ create new facebook archives for newsfeed from a fbid.
         Args:
             request (str, int, str): [fbid, num, include_text]
        """
        fbid = request.json.get('fbid')
        include_text = request.json.get('include')
        num = sint(request.json.get('num', 20), 20)
        data = await archive_feed_by_filter(fbid, num, include_text, self.ap)

        return json(data, ensure_ascii=False)

async def archive_feed_by_filter(fbid, num, include_text, ap=None, name=None):
    from fbfeed.filter import FbFeedFilter
    if not ap:
        from db.providers import FacebookArchiveProvider
        ap = FacebookArchiveProvider()

    items = await FbFeedFilter(fbid, num, include_text, search=True).as_output()
    total = len(items)
    # checking duplicate items by hash
    items = await ap.as_find_distinct_items_by("hash", items)
    ids = list(await ap.as_save_all(items))
    acceptances = len(ids)
    rejects = total - acceptances

    return dict_cleaner(None, {
        'source': fbid,
        'include': include_text,
        'acceptances': acceptances,
        'rejects': rejects,
        'items': ids,
        'info': '(%d/%d)' % (acceptances, total),
        'infomation': '(%d/%d) %d successfully created, %d duplicates found.' % (acceptances, total, acceptances, rejects)
    })
