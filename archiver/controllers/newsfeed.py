from sanic.response import json
from sanic.views import HTTPMethodView

from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc

from newsfeed.utils.newsfeed_helper import fetch_feed

class NewsfeedController(HTTPMethodView):

    async def post(self, request):
        """ create new archive for newsfeed.
         Args:
             request (str): contains a str of feed url.
         Returns:
             json: containing key `status` with success/failure message
        """

        url = request.json.get('url')
        items = fetch_feed(url, full_text=False)
        hashs = [item['hash'] for item in items]
        ok_nums = len(items)
        dup_nums = ok_nums
        #checking duplicate items by hash
        with query_session() as session:
            result_set = session.query(Archive).filter(Archive.hash.in_(hashs)).all()
            dups = [dup.__dict__['hash'] for dup in result_set]
            objs = [Archive(**item) for item in items if item['hash'] not in dups]
            ok_nums = len(objs)

        #checking duplicate items by IntegrityError
        with scoped_session() as session:
            for obj in objs:
                try:
                   with session.begin_nested():
                        session.add(obj)
                except exc.IntegrityError:
                    ok_nums = ok_nums - 1
            dup_nums = dup_nums - ok_nums

        return json({'status': 'ok', 'nums': ok_nums, 'info': 'Successfully created %d news archives, found %d duplicate items' % (ok_nums, dup_nums)})
