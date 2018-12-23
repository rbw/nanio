# -*- coding: utf-8 -*-

from sanic.views import HTTPMethodView
from nanio.config import APP_DEBUG


class NanioController(HTTPMethodView):
    svc = None

    def dispatch_request(self, req, *args, **kwargs):
        # TODO: Inject remote_addr? Too much OH? -- Benchmark
        # self.svc.log = LoggerAdapter(self.svc.log, {'remote_addr': req.remote_addr or req.ip})
        return super(NanioController, self).dispatch_request(req, *args, **kwargs)

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))


class NanioPackage:
    def __init__(self, name, controllers, service, documents):
        self.name = name
        self.db_name = 'nanio__'.format(name)

        self.controllers = controllers
        self.documents = documents
        self.svc = service

    def __repr__(self):
        return '<NanioPackage [{0}] at {1}>'.format(self.name, hex(id(self)))


class NanioService:
    debug = APP_DEBUG

    def __init__(self, http_client, docs, log, pkg):
        self.http_client = http_client
        self.docs = docs
        self.log = log
        self.pkg = pkg

    async def http_post(self, url, payload):
        async with self.http_client.post(url, data=payload) as resp:
            result = await resp.json()
            return result, resp.status

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))
