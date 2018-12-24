# -*- coding: utf-8 -*-

from sanic import response
from nanio.pkg import NanioController


class UIController(NanioController):
    path_relative = '/'

    async def get(self, req):
        resp = await self.svc.schemas
        return response.json(resp, 200)
