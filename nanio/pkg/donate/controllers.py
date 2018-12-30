# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetfactoryController, Route


class DonationController(JetfactoryController):
    def __init__(self):
        self.routes = [
            Route(handler=self.one, path='/', method='GET', schema=None)
        ]

    async def one(self, req):
        # resp = await self.svc.process_donation(req)
        return jsonify({}, 200)

