from sanic.response import json
from sanic.views import HTTPMethodView

from db.database import scoped_session, Session
from db.models.archives import Archive


class NewsfeedController(HTTPMethodView):

    async def post(self, request):
        """ create new archive for newsfeed.
         Args:
             request (list): contains a list of feed url.
         Returns:
             json: containing key `status` with success info
        """
        url = request.json.get('url')

        data = {
            'published': "",
            'title': "",
            'summary': "",
            'link': ""
        }

        # Create new archive.
        with scoped_session() as session:
            archive = Archive(data)
            session.add(archive)

        # Return json response.
        return json({'msg': 'Successfully created {}'.format(email)})
