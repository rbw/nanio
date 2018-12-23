# -*- coding: utf-8 -*-

from sanic import response
from nanio.ext import NanioController


class DonationController(NanioController):
    path_relative = '/'

    async def get(self, req):
        resp = await self.svc.process_donation(req)
        return response.json(resp, 200)
