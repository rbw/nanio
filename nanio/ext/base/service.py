# -*- coding: utf-8 -*-

from nanio.config import APP_DEBUG
from umongo import MotorAsyncIOInstance


class NanioService:
    __db__ = None

    motor = None
    umongo = None

    http_client = None
    log = None

    debug = APP_DEBUG

    def models_register(self, models):
        self.__db__ = MotorAsyncIOInstance()
        for model in models:
            self.__db__.register(model, as_attribute=True)

    @classmethod
    async def http_post(cls, url, payload):
        async with cls.http_client.post(url, data=payload) as resp:
            result = await resp.json()
            return result, resp.status
