# -*- coding: utf-8 -*-

from sanic import Blueprint, response
from nanio.services import nano_service

bp = Blueprint(__name__, url_prefix='/node-rpc')


@bp.route('/', methods=['POST'])
async def post(request):
    relay_result, status = await nano_service.send(request.json)
    return response.json(relay_result, status=status)
