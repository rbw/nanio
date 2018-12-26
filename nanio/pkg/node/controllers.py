# -*- coding: utf-8 -*-

from sanic import response
from nanio.config import RPC_ENABLED
from nanio.pkg import Route, Methods
from nanio.pkg.templates import NanioController


class NodeController(NanioController):
    def __init__(self):
        super(NodeController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.schemas),
            Route(path='/', method=Methods.POST, handler=self.relay)
        )

    async def schemas(self, _):
        return response.json(self.svc.schemas.by_category, 200)

    async def relay(self, req):
        if not RPC_ENABLED:
            return {'result': 'RPC relay disabled'}, 200

        relay_result, status = await self.svc.send(req.json, is_internal=False)
        return response.json(relay_result, status=status)
