from sanic.response import json
from sanic.views import HTTPMethodView
from utils.data_utils import dict_cleaner
from crawler.utils.crawler_helper import as_fetch_news
from crawler.utils.crawler_utils import detect_news_source
import settings


class NewsfeedController(HTTPMethodView):

    from db.providers import ArchiveProvider
    ap = ArchiveProvider()

    async def get(self, request, hashid):
        """ show archive by hashid
         Args:
             hashid: contains a str of hashed id.
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

    async def put(self, request):
        """ update archives for newsfeed from a news url.
         Args:
             request (str): [url]
        """
        url = request.json.get('url')
        data = await as_fetch_news(url)
        if data['pass']:
            ids = await self.ap.as_update(data)
            return json({'item': ids}, ensure_ascii=False)

    async def delete(self, request, hashid):
        """ delete an archive by hashid.
         Args:
            hashid: contains a str of hashed id.
            request (str): [key]
        """
        delete_key = request.json.get('key')

        if not settings.DELETE_KEY or delete_key != settings.DELETE_KEY:
            data = {'auth': False}
        else:
            data = {
                'auth': True,
                'deleted': await self.ap.as_remove(hashid)
            }
        return json(data, ensure_ascii=False)


async def archive_feed_by_filter(url, include_text, ap=None, connections=None):
    from newsfeed.filter import NewsFeedFilter
    if not ap:
        from db.providers import ArchiveProvider
        ap = ArchiveProvider()

    items = await NewsFeedFilter(url, include_text, full_text=True, connections=connections).as_output()

    total = len(items)
    # checking duplicate items by hash
    items = await ap.as_find_distinct_items_by("hash", items)
    ids = list(await ap.as_save_all(items))
    acceptances = len(ids)
    rejects = total - acceptances

    return dict_cleaner(None, {
        'source': detect_news_source(url),
        'url': url,
        'include': include_text,
        'acceptances': acceptances,
        'rejects': rejects,
        'items': ids,
        'info': '(%d/%d)' % (acceptances, total),
        'infomation': '(%d/%d) %d successfully created, %d duplicates found.' % (acceptances, total, acceptances, rejects)
    })
