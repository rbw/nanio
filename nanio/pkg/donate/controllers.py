# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import Route, Methods, JetfactoryController


class DonationController(JetfactoryController):
    def __init__(self):
        super(DonationController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.one)
        )

    async def one(self, req):
        print(req)
        # resp = await self.svc.process_donation(req)
        return jsonify({}, 200)

