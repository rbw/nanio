# -*- coding: utf-8 -*-

from nanio.log import log_api
from nanio.config import APP_DEBUG


class NanioService:
    debug = APP_DEBUG
    log = log_api
    http_client = None

    @classmethod
    def set_http_client(cls, client):
        cls.http_client = client

    @classmethod
    async def http_post(cls, url, payload):
        async with cls.http_client.post(url, data=payload) as resp:
            result = await resp.json()
            return result, resp.status
