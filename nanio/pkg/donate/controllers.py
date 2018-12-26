# -*- coding: utf-8 -*-

from sanic import response
from nanio.pkg import Route, Methods
from nanio.pkg.templates import NanioController


class DonationController(NanioController):
    def __init__(self):
        super(DonationController, self).__init__(
            Route(path='/', method=Methods.GET, handler=self.one)
        )

    async def one(self, req):
        print(req)
        # resp = await self.svc.process_donation(req)
        return response.json({}, 200)

