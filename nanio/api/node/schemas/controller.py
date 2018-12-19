# -*- coding: utf-8 -*-

from sanic import Blueprint, response
from nanio.services import nano_service

bp = Blueprint(__name__, url_prefix='/schemas')


@bp.route('/', methods=['GET'])
async def get(_):
    return response.json(nano_service.schemas.by_category, 200)
