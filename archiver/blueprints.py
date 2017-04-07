from sanic.response import text
from sanic import Blueprint
from archiver.controllers import NewsfeedController
from archiver.controllers import NewsfeedListController
from archiver.controllers import FbfeedController
from archiver.controllers import FbfeedListController

bp_v1 = Blueprint('v1', url_prefix='/api/v1')


@bp_v1.route('/')
async def api_v1_root(request):
    return text('ARCHIVE SERIES API VERSION 1')

bp_v1.add_route(NewsfeedController().as_view(), '/archive/news', methods=['POST'])
bp_v1.add_route(NewsfeedController().as_view(), '/archive/news/<hashid>', methods=['GET'])
bp_v1.add_route(NewsfeedListController().as_view(), '/archive/news/list', methods=['GET'])

bp_v1.add_route(FbfeedController().as_view(), '/archive/facebook', methods=['POST'])
bp_v1.add_route(FbfeedController().as_view(), '/archive/facebook/<hashid>', methods=['GET'])
bp_v1.add_route(FbfeedListController().as_view(), '/archive/facebook/list', methods=['GET'])
