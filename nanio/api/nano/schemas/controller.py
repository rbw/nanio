# -*- coding: utf-8 -*-

from sanic import Blueprint, response
from nanio.services import nano_service

bp = Blueprint(__name__, url_prefix='/schemas')


@bp.route('/', methods=['GET'])
async def get(request):
    schemas = await nano_service.get_rpc_schemas()
    return response.json(schemas, 200)
