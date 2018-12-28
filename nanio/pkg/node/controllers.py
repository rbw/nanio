# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetfactoryController, Route, Methods

from nanio.settings import RPC_ENABLED


class NodeController(JetfactoryController):
    def __init__(self):
        super(NodeController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.schemas),
            Route(path='/', method=Methods.POST, handler=self.relay)
        )

    async def schemas(self, _):
        return jsonify(self.svc.schemas.by_category, 200)

    async def relay(self, req):
        if not RPC_ENABLED:
            return {'result': 'RPC relay disabled'}, 200

        relay_result, status = await self.svc.send(req.json, is_internal=False)
        return jsonify(relay_result, status=status)
