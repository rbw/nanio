# -*- coding: utf-8 -*-

from nanio.config import APP_DEBUG


class NanioService:
    debug = APP_DEBUG

    def __init__(self, docs, log, pkgs, app):
        self.docs = docs
        self.log = log
        self.pkgs = pkgs
        self.app = app

    async def http_post(self, url, payload):
        async with self.app.http_client.post(url, data=payload) as resp:
            result = await resp.json()
            return result, resp.status

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))
