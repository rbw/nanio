# -*- coding: utf-8 -*-

from sanic import response, views
from nanio.log import Log
from nanio.utils import inject_log_meta


class SchemaAPI(views.HTTPMethodView):
    log = Log.node_rpc

    @inject_log_meta
    async def get(self, request):
        self.log.info('Sending frontend config')

        return response.json({
            'rpc': request.app.rpc_schema
        }, 200)
