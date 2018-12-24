import ujson
import aiohttp
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance as DatabaseInstance

from sanic import Sanic, response
from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.log import LOGGING_CONFIG_DEFAULTS, log_root


def server_start(app, loop):
    mongodb_address = '{0}:{1}'.format(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])

    # Reuse the server loop for motor and aiohttp
    app.motor = motor = AsyncIOMotorClient(mongodb_address, io_loop=loop)
    app.http_client = http_client = aiohttp.ClientSession(loop=loop)

    for pkg in dict(app.packages).values():
        # Documents needs to be ready before service instantiation
        docs = DatabaseInstance(motor[pkg.name])
        for document in pkg.documents:
            registered = docs.register(document, as_attribute=True)
            registered.ensure_indexes()

        # Create instance of the package Service and inject useful stuff.
        pkg.svc = pkg.svc(
            http_client=http_client,
            docs=docs,
            log=logging.getLogger('nanio.api.{0}'.format(pkg.name)),
            pkg=app.packages,
        )

        # Add routes and inject Service.
        for ctrl in pkg.controllers:
            rp = ctrl.path_relative
            ctrl.svc = pkg.svc

            # URL path formatter
            path = '{0}/{1}/{2}'.format(
                app.base_path,
                pkg.name,
                rp[1:] if rp.startswith('/') else rp
            ).rstrip('/')

            app.add_route(ctrl.as_view(), path)


def server_stop(app, loop):
    app.motor.close()
    loop.close()


def register_error_handlers(app):
    @app.exception(SanicException)
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

    def __init__(self, packages=None, **kwargs):
        super(Nanio, self).__init__(
            kwargs.pop('name', 'nanio'),
            log_config=kwargs.pop('log_config', LOGGING_CONFIG_DEFAULTS),
            **kwargs
        )

        # Provides a registry for convenient access and error handling
        if not isinstance(packages, list):
            raise Exception('Nanio expects a list of packages.')

        self.packages.load(packages)

        # Read ENV-YML config
        self.config.from_object(nanio.config)

        # Register error handler for catching exceptions and converting to JSON formatted errors
        register_error_handlers(self)

        # Startup listener -- package registration (controllers, documents, services etc).
        self.register_listener(server_start, 'before_server_start')

        # Shutdown listener
        self.register_listener(server_stop, 'after_server_stop')

