# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import Route, Methods, JetfactoryController


class UIController(JetfactoryController):
    def __init__(self):
        super(UIController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.get)
        )

    async def get(self, req):
        node_schemas = self.svcs.node.schemas.by_category
        response = await self.svc.get_schemas(node_schemas)
        return jsonify(response)
