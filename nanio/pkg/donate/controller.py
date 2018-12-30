# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.base import JetController, JetControllerSettings, JetRoute


class DonationController(JetController):
    def _setup(self):
        return JetControllerSettings(
            path='/donations',
            routes=[
                JetRoute(handler=self.one, path='/', method='GET', schema=None)
            ]
        )

    async def one(self, req):
        # resp = await self.svc.process_donation(req)
        return jsonify({}, 200)

