from sanic.response import json
from sanic.views import HTTPMethodView
from utils.data_utils import dict_cleaner, data_hasher
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

    async def put(self, request, hashid):
        """ update archives by hashid and news url.
        Args:
            hashid: contains a str of hashed id.
            request (str): [url]
        """
        delete_key = request.json.get('key')
        data = {'auth': False}

        if not settings.DELETE_KEY or delete_key != settings.DELETE_KEY:
            pass
        else:
            url = request.json.get('url')
            item = await as_fetch_news(url)
            if item['pass']:
                data = {
                    'auth': True,
                    'updated': await self.ap.as_update(hashid, item)
                }

        return json(data, ensure_ascii=False)

    async def delete(self, request, hashid):
        """ delete an archive by hashid.
        Args:
            hashid: contains a str of hashed id.
            request (str): [key]
        """
        delete_key = request.json.get('key')
        data = {'auth': False}
        if not settings.DELETE_KEY or delete_key != settings.DELETE_KEY:
            pass
        else:
            data = {
                'auth': True,
                'deleted': await self.ap.as_remove(hashid)
            }
        return json(data, ensure_ascii=False)


async def archive_feed_by_filter(url, include_text, ap=None, osp=None, connections=None):
    from newsfeed.filter import NewsFeedFilter
    if not ap:
        from db.providers import ArchiveProvider
        ap = ArchiveProvider()
    if not osp:
        from db.providers import ObserverStatProvider
        osp = ObserverStatProvider()

    nff = NewsFeedFilter(url, include_text, full_text=True, connections=connections)
    items = await nff.as_output()
    count = nff.feedCount()
    total = len(items)
    # checking duplicate items by hash
    items = await ap.as_find_distinct_items_by("hash", items)
    ids = list(await ap.as_save_all(items))
    acceptances = len(ids)
    rejects = total - acceptances

    await osp.as_save({
        'count': count,
        'total': total,
        'acceptances': acceptances,
        'rejects': rejects
    })

    return dict_cleaner(None, {
        'source': detect_news_source(url),
        'url': url,
        'include': include_text,
        'count': count,
        'total': total,
        'acceptances': acceptances,
        'rejects': rejects,
        'items': ids,
        'info': '(%d/%d)' % (acceptances, total),
        'infomation': '(%d/%d) %d successfully created, %d duplicates found.' % (acceptances, total, acceptances, rejects)
    })
