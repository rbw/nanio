# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetController, JetRoute, JetControllerSettings


class UIController(JetController):
    def __init__(self):
        self.node_svc = self.pkgs.get('node').svc

    def _setup(self):
        return JetControllerSettings(
            path='/',
            routes=[
                JetRoute(handler=self.get, path='/', method='GET', schema=None)
            ]
        )

    async def get(self, req):
        print(self.node_svc.schemas.by_category)
        # response = self.svc.get_schemas(svc.schemas.by_category)
        return jsonify(self.node_svc.schemas.by_category)
