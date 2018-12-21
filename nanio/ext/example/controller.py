# -*- coding: utf-8 -*-

from sanic import response
from nanio.ext import BaseController


class ExampleController(BaseController):
    path_relative = '/'

    async def get(self, req):
        cursor = self.svc.docs.Example.find()
        print(await cursor.to_list(10))

        return response.json({}, 200)
