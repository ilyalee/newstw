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
        save_nums = len(items)
        dup_nums = save_nums
        #checking duplicate items by hash
        with query_session() as session:
            result_set = session.query(Archive).filter(Archive.hash.in_(hashs)).all()
            dups = [dup.__dict__['hash'] for dup in result_set]
            items = [item for item in items if item['hash'] not in dups]
            archives = [Archive(**item) for item in items]
            save_nums = len(archives)

        #checking duplicate items by IntegrityError
        with scoped_session() as session:
            for archive in archives:
                try:
                   with session.begin_nested():
                        session.add(archive)
                except exc.IntegrityError:
                    save_nums = save_nums - 1
            dup_nums = dup_nums - save_nums

        data = {
            'save_nums': save_nums,
            'dup_nums': dup_nums,
            'items': items,
            'info': '%d successfully created, %d duplicates found.' % (save_nums, dup_nums)
        }

        return json(data)
