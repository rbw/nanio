# -*- coding: utf-8 -*-

from sanic import response
from pkg.templates import NanioController


class UIController(NanioController):
    path = '/'
    schema = 'schema'

    async def get(self, _):
        resp = await self.svc.get_schemas()
        return response.json(resp, 200)
