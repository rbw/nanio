# -*- coding: utf-8 -*-

import ujson

from logging import LoggerAdapter
from sanic import Sanic, response

from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.log import LOGGING_CONFIG_DEFAULTS, Log
from nanio.api import base, gateway

log = Log.root


def register_error_handlers(app):
    @app.exception(SanicException)
    async def sanic_error(_, exception):
        msg = exception.__str__()

        if isinstance(exception, NanioException):
            if exception.log_message:
                log.error(msg)

        try:
            error = ujson.loads(msg)
        except ValueError:
            error = msg

        return response.json(body={'error': error}, status=exception.status_code)


async def contextual_logging(request):
    Log.api = LoggerAdapter(Log.api, {'remote_addr': request.remote_addr or request.ip})


def create_app():
    app = Sanic('nanio', log_config=LOGGING_CONFIG_DEFAULTS)
    app.config.from_object(nanio.config)
    register_error_handlers(app)
    app.register_middleware(contextual_logging, 'request')

    # Register base /api
    app.blueprint(base)

    # Register Node RPC API gateway
    app.blueprint(gateway)

    log.info('Nanio starting...')

    if app.config['RPC_ENABLED']:
        log.info('RPC backends: {0}'.format(','.join(app.config['RPC_NODES']) or 'None configured'))
    else:
        log.info('RPC proxy disabled')

    return app
