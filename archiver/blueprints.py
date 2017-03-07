from sanic.response import text
from sanic import Blueprint
from archiver.controllers.newsfeed import NewsfeedController

bp_v1 = Blueprint('v1', url_prefix='/api/v1')


@bp_v1.route('/')
async def api_v1_root(request):
    return text('NEWSFEED API VERSION 1')

bp_v1.add_route(NewsfeedController().as_view(), '/archive', methods=['POST'])
bp_v1.add_route(NewsfeedController().as_view(), '/archive/<hashid>', methods=['GET'])
