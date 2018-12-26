# -*- coding: utf-8 -*-

from sanic.blueprints import FutureRoute


class NanioController:
    svc = None

    def __init__(self, *routes):
        self.routes = []
        for handler, path, method in routes:
            self.routes.append(
                FutureRoute(
                    handler=handler, uri=path, methods=[method.value],
                    host=None, strict_slashes=False, stream=None,
                    version=None, name=handler.__name__
                )
            )

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, hex(id(self)))
