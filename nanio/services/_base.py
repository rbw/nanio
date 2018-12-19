# -*- coding: utf-8 -*-

import aiohttp
from nanio.log import Log
from nanio.config import APP_DEBUG


class Service:
    url = None
    debug = APP_DEBUG
    log = Log.api

    async def http_post(self, payload):
        async with aiohttp.ClientSession().post(self.url, data=payload) as resp:
            result = await resp.json()
            return resp.status, result
