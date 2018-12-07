# -*- coding: utf-8 -*-

from logging import LoggerAdapter
from sanic import response, views
from nanio.log import Log


def inject_log_meta(func):
    def inner(self, request, *args, **kwargs):
        self.log = LoggerAdapter(self.log, {'host': request.ip})
        return func(self, request, *args, **kwargs)

    return inner


class UIView(views.HTTPMethodView):
    log = Log.node_rpc

    @inject_log_meta
    async def get(self, request):
        self.log.info('Sending frontend config')

        return response.json({
            'rpc': request.app.rpc_defs
        }, 200)
