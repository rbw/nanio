# -*- coding: utf-8 -*-

from sanic import response
from nanio.pkg import Route, Methods
from nanio.pkg.templates import NanioController


class UIController(NanioController):
    def __init__(self):
        super(UIController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.get)
        )

    async def get(self, req):
        resp = await self.svc.get_schemas()
        return response.json(resp, 200)
