# -*- coding: utf-8 -*-

import ujson
import aiohttp
import logging
import re

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance as DatabaseInstance

from sanic import Sanic, response
from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.log import LOGGING_CONFIG_DEFAULTS, log_root


def format_path(*parts):
    path = ''

    for part in parts:
        path = '/{0}/{1}'.format(path, part)

    return re.sub(r'/+', '/', path.rstrip('/'))


async def server_start(app, loop):
    # Start motor and inject into app
    mongodb_address = '{0}:{1}'.format(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
    app.motor = AsyncIOMotorClient(mongodb_address, io_loop=loop)

    for pkg in dict(app.packages).values():
        # Documents needs to be ready before service instantiation
        docs = DatabaseInstance(app.motor[pkg.collection])
        for document in pkg.documents:
            registered = docs.register(document, as_attribute=True)
            registered.ensure_indexes()

        # Create instance of the package Service and inject useful stuff.
        pkg.svc = pkg.svc(
            docs=docs,
            log=logging.getLogger('nanio.api.{0}'.format(pkg.name)),
            pkgs=app.packages,
            app=app,
        )

        pkg.controller.svc = pkg.svc

        for route in pkg.controller.routes:
            app.route(uri=format_path(app.base_path, pkg.path, route.uri),
                      methods=route.methods,
                      host=route.host,
                      strict_slashes=route.strict_slashes,
                      stream=route.stream,
                      version=route.version,
                      name=route.name,
                      )(route.handler)

    # Reuse the server loop for motor and aiohttp
    app.http_client = aiohttp.ClientSession(loop=loop)


# Raise an exception during bootstrapping to reproduce.
async def before_server_stop(app, loop):
    await app.http_client.close()


class PackageRegistry:
    _packages = {}

    def load(self, packages):
        self._packages = {e.name: e for e in packages}

    def __iter__(self):
        yield from self._packages.items()

    def __repr__(self):
        return '<{0} {1} at {2}>'.format(self.__class__.__name__, list(self._packages.keys()), hex(id(self)))

    def __getattr__(self, item):
        if item not in self._packages:
            raise Exception('No such package: {0}'.format(item))

        return self._packages.get(item)


class Nanio(Sanic):
    http_client = None
    motor = None
    base_path = '/api'
    packages = PackageRegistry()

    def register_error_handlers(self):
        @self.exception(SanicException)
        async def nanio_error(_, exception):
            msg = exception.__str__()

            if isinstance(exception, NanioException):
                if exception.log_message:
                    log_root.error(msg)

            try:
                error = ujson.loads(msg)
            except ValueError:
                error = msg

            return response.json(body={'error': error}, status=exception.status_code)

    def __init__(self, packages=None, **kwargs):
        super(Nanio, self).__init__(
            kwargs.pop('name', 'nanio'),
            log_config=kwargs.pop('log_config', LOGGING_CONFIG_DEFAULTS),
            **kwargs
        )

        # Provides a registry for convenient access and error handling
        if not isinstance(packages, list):
            raise Exception('Nanio expects a list of packages.')

        # Lazy load packages, init later upon loop start
        self.packages.load(packages)

        # Reads config of ENV or YML into app
        self.config.from_object(nanio.config)

        # Register error handler for catching exceptions and converting to JSON formatted errors
        self.register_error_handlers()

        # Startup listener -- package registration (controllers, documents, services etc).
        self.register_listener(server_start, 'before_server_start')

        # Shutdown listener
        self.register_listener(before_server_stop, 'before_server_stop')
