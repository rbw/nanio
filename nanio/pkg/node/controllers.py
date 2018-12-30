# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetfactoryController, Route


class NodeController(JetfactoryController):
    def setup(self):
        # The (RPC) relay route handles validation / (de)serialization in the service layer
        return [
            Route(handler=self.schemas, path='/', method='GET', schema=None),
            Route(handler=self.relay, path='/', method='POST', schema=None)
        ]

    async def schemas(self, _):
        return jsonify(self.svc.schemas.by_category, 200)

    async def relay(self, req):
        if not self.cfg['enabled']:
            return {'result': 'RPC relay disabled'}, 200

        relay_result, status = await self.svc.send(req.json, is_internal=False)
        return jsonify(relay_result, status=status)
