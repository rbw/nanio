# -*- coding: utf-8 -*-

from sanic.views import HTTPMethodView


class NanioController(HTTPMethodView):
    svc = None
    routes = {
        'GET': [],
        'POST': [],
        'PUT': [],
        'PATCH': [],
        'DELETE': [],
    }

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))
