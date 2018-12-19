# -*- coding: utf-8 -*-

from sanic import Blueprint, response
from nanio.config import RPC_ENABLED


bp = Blueprint('node', url_prefix='/node')


@bp.route('/', methods=['GET'])
async def get(req):
    node = req.app.ext['node']
    node.log.debug('Sending node RPC schemas...')
    return response.json(node.schemas.by_category, 200)


@bp.route('/', methods=['POST'])
async def post(req):
    if not RPC_ENABLED:
        return {'result': 'RPC gateway is disabled'}, 200

    relay_result, status = await req.app.ext['node'].send(req.json)
    return response.json(relay_result, status=status)
