# -*- coding: utf-8 -*-

from sanic.views import HTTPMethodView
from nanio.config import APP_DEBUG


class BaseController(HTTPMethodView):
    view = None
    svc = None
    db = None
    ext = {}

    def dispatch_request(self, req, *args, **kwargs):
        # TODO: Inject remote_addr? Is it worth the overhead?
        # self.svc.log = LoggerAdapter(self.svc.log, {'remote_addr': req.remote_addr or req.ip})
        return super(BaseController, self).dispatch_request(req, *args, **kwargs)


class Extension:
    def __init__(self, name, controllers, service, documents):
        self.name = name
        self.db_name = 'nanio__'.format(name)

        self.controllers = controllers
        self.documents = documents
        self.svc = service


class BaseService:
    docs = None
    log = None
    http_client = None
    debug = APP_DEBUG

    async def http_post(self, url, payload):
        async with self.http_client.post(url, data=payload) as resp:
            result = await resp.json()
            return result, resp.status
