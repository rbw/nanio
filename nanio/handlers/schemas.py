# -*- coding: utf-8 -*-

from sanic import response, views
from nanio.log import Log
from nanio.utils import inject_log_meta


class SchemasAPI(views.HTTPMethodView):
    log = Log.node_rpc

    @inject_log_meta
    async def get(self, request):
        self.log.info('GET RPC schemas')
        return response.json(request.app.config['RPC_SCHEMAS'], 200)
