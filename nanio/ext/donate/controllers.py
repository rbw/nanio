# -*- coding: utf-8 -*-

from sanic import response
from nanio.ext import BaseController


class DonateController(BaseController):
    path_relative = '/'

    async def get(self, req):
        wallet = await self.svc.docs.Wallet.find_one()
        if not wallet:
            pass

        print(self.svc)
        # await self.svc.send()

        # print(await cursor.to_list(10))

        return response.json({}, 200)
