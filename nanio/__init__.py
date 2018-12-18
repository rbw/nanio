# -*- coding: utf-8 -*-

import logging
import logging.config
import ujson

from sanic import Sanic, response

from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

import nanio.config
from nanio.handlers import NodeGateway, SchemasAPI
from nanio.schemas import RPCSettings, get_rpc_schemas
from nanio.log import LOGGING_CONFIG_DEFAULTS, Log


def register_error_handlers(app):
    @app.exception(SanicException)
    async def sanic_error(_, exception):
        msg = exception.__str__()

        if isinstance(exception, NanioException):
            if exception.log_message:
                Log.error.info(msg)

        try:
            error = ujson.loads(msg)
        except ValueError:
            error = msg

        return response.json(body={'error': error}, status=exception.status_code)


def create_app():
    # Create app
    app = Sanic('nanio', log_config=LOGGING_CONFIG_DEFAULTS)
    app.config.from_object(nanio.config)

    # Set up logging
    """logging.config.dictConfig(app.log_config)
    loglevel = 'DEBUG' if app.cfg.core['debug'] else 'INFO'

    for name in LOGGING_CONFIG_DEFAULTS['loggers'].keys():
        logging.getLogger(name).setLevel(loglevel)"""

    # Show some useful details
    Log.root.info('Nanio starting...')

    """if app.cfg.rpc['enabled']:
        Log.root.info('RPC backends: {0}'.format(','.join(app.rpc_nodes) or 'None configured'))
    else:
        Log.root.info('RPC proxy disabled')"""

    # Register routes
    app.add_route(NodeGateway.as_view(app.config), '/node-rpc')
    app.add_route(SchemasAPI.as_view(), '/api/schemas')

    register_error_handlers(app)

    return app
