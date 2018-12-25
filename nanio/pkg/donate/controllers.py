# -*- coding: utf-8 -*-

from sanic import response
# from pkg.templates import NanioController
from .schemas import DonationQuerySchema

from functools import wraps, partial
from sanic.views import HTTPMethodView


class NanioController(HTTPMethodView):
    svc = None
    resources = []

    @classmethod
    def add_resource(cls, *resource):
        cls.resources.append(resource)

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))


def get(route, *args, **kwargs):
    return resource(route, 'GET', *args, **kwargs)


def resource(path, method, *args, **kwargs):
    # validate = kwargs.pop('validate', True)
    schema = kwargs.pop('schema')

    def decorator(f):
        @wraps(f)
        def handler(*inner_args, **inner_kwargs):
            print(NanioController.resources)

            return f(*inner_args, **inner_kwargs)

        NanioController.add_resource(method, path, decorator)

        return f

    return decorator


class DonationController(NanioController):
    @get('/', schema=DonationQuerySchema)
    async def one(self, req):
        # resp = await self.svc.process_donation(req)
        return response.json({}, 200)
