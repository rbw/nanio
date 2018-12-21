# -*- coding: utf-8 -*-

from sanic import response
from nanio.config import RPC_ENABLED
from nanio.ext import BaseController


class NodeController(BaseController):
    path_relative = '/'

    async def get(self, req):
        # cursor = self.svc.db.Test.find()
        # print(await cursor.to_list(10))
        return response.json(self.svc.schemas.by_category, 200)

    async def post(self, req):
        if not RPC_ENABLED:
            return {'result': 'RPC relay disabled'}, 200

        relay_result, status = await self.svc.send(req.json)
        return response.json(relay_result, status=status)
