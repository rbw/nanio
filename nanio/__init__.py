import ujson
import aiohttp
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance

from sanic import Sanic, response
from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.log import LOGGING_CONFIG_DEFAULTS, log_root


def server_start(app, loop):
    app.motor = motor = AsyncIOMotorClient(app.config['MONGODB_HOST'], io_loop=loop)
    app.http_client = http_client = aiohttp.ClientSession(loop=loop)

    for ext in app.extensions.values():
        ext.svc.http_client = http_client
        ext.svc.db = Instance(motor[ext.name])
        ext.svc.log = logging.getLogger('nanio.api.{0}'.format(ext.name))
        ext.svc.ext = app.extensions

        for ctrl in ext.controllers:
            rp = ctrl.path_relative
            ctrl.svc = ext.svc

            # URL path formatter
            path = '{0}/{1}/{2}'.format(
                app.base_path,
                ext.name,
                rp[:-1] if rp.startswith('/') else rp
            ).rstrip('/')

            app.add_route(ctrl.as_view(), path)

        for document in ext.documents:
            ext.svc.db.register(document, as_attribute=True)


def server_stop(app, loop):
    app.motor.close()
    loop.close()


class Nanio(Sanic):
    http_client = None
    motor = None
    extensions = {}
    base_path = '/api'

    def __init__(self, **kwargs):
        super(Nanio, self).__init__(
            kwargs.pop('name', 'nanio'),
            log_config=kwargs.pop('log_config', LOGGING_CONFIG_DEFAULTS),
            **kwargs
        )
        self.config.from_object(nanio.config)

        # Register error handler for catching exceptions and converting to JSON formatted errors
        self.register_error_handlers()

        # Register aiohttp client
        self.register_listener(server_start, 'before_server_start')
        self.register_listener(server_stop, 'after_server_stop')

    def register_error_handlers(self):
        @self.exception(SanicException)
        async def sanic_error(_, exception):
            msg = exception.__str__()

            if isinstance(exception, NanioException):
                if exception.log_message:
                    log_root.error(msg)

            try:
                error = ujson.loads(msg)
            except ValueError:
                error = msg

            return response.json(body={'error': error}, status=exception.status_code)

    def register_extensions(self, extensions):
        for extension in extensions:
            self.extensions[extension.name] = extension

