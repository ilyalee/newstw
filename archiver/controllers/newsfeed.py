from sanic.response import json
from sanic.views import HTTPMethodView
from utils.data_utils import dict_cleaner
from crawler.utils.crawler_utils import detect_news_source


class NewsfeedController(HTTPMethodView):

    from db.providers.archive_provider import ArchiveProvider
    ap = ArchiveProvider()

    async def get(self, request, hashid):
        """ show archive by hashid
         Args:
             hashed: contains a str of hashed id.
        """
        item = await self.ap.as_load(hashid, ['id', 'hash'])

        return json(item, ensure_ascii=False)

    async def post(self, request):
        """ create new archives for newsfeed from a feed url.
         Args:
             request (str, str): [url, include_text]
        """
        url = request.json.get('url')
        include_text = request.json.get('include')
        data = await archive_feed_by_filter(url, include_text, self.ap)

        return json(data, ensure_ascii=False)

async def archive_feed_by_filter(url, include_text, ap=None):
    from newsfeed.filter import NewsFeedFilter
    if not ap:
        from db.providers.archive_provider import ArchiveProvider
        ap = ArchiveProvider()

    feed = NewsFeedFilter(url, include_text, full_text=True)
    items = await feed.as_output()
    total = len(items)

    # checking duplicate items by hash
    items = await ap.as_find_distinct_items_by("hash", items)
    ids = await ap.as_save_all(items)
    acceptances = len(ids)
    rejects = total - acceptances

    data = dict_cleaner(None, {
        'source': detect_news_source(url),
        'url': url,
        'include': include_text,
        'acceptances': acceptances,
        'rejects': rejects,
        'items': ids,
        'info': '%d successfully created, %d duplicates found.' % (acceptances, rejects)
    })

    return data
