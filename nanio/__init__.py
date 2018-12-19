# -*- coding: utf-8 -*-

import ujson
import aiohttp

from logging import LoggerAdapter
from sanic import Sanic, response

from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.log import LOGGING_CONFIG_DEFAULTS, log_root, log_api
from nanio.ext import registry, NanioService


def register_error_handlers(app):
    @app.exception(SanicException)
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


async def client_create(app, loop):
    app.http_client = aiohttp.ClientSession(loop=loop)
    NanioService.set_http_client(app.http_client)


async def client_destroy(app, loop):
    loop.run_until_complete(app.http_client.close())
    loop.close()


async def contextual_logging(request):
    NanioService.log = LoggerAdapter(log_api, {'remote_addr': request.remote_addr or request.ip})


def create_app():
    app = Sanic('nanio', log_config=LOGGING_CONFIG_DEFAULTS)
    app.config.from_object(nanio.config)

    # Register error handler for catching exceptions and converting to JSON formatted errors
    register_error_handlers(app)

    # Add contextual logger middleware
    app.register_middleware(contextual_logging, 'request')

    # Register aiohttp client
    app.register_listener(client_create, 'before_server_start')
    app.register_listener(client_destroy, 'after_server_stop')

    # Add extension registry to app
    app.ext = registry

    # Register blueprints from AppRegistry
    app.blueprint(registry.blueprints)

    log_root.info('Nanio starting...')

    if app.config['RPC_ENABLED']:
        log_root.info('RPC backends: {0}'.format(','.join(app.config['RPC_NODES']) or 'None configured'))
    else:
        log_root.info('RPC proxy disabled')

    return app
