# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetfactoryController, Route


class UIController(JetfactoryController):
    def setup(self):
        return [
            Route(handler=self.get, path='/', method='GET', schema=None)
        ]

    async def get(self, req):
        svc = self.app.pkgs['node'].svc
        print(svc.schemas.by_category)
        # response = self.svc.get_schemas(svc.schemas.by_category)
        return jsonify(svc.schemas.by_category)
