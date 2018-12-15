# -*- coding: utf-8 -*-

import logging
import logging.config
import ujson
import shelve

from os import environ as env
from yaml import load as yaml_parse
from yaml.parser import ParserError as YAMLParseError

from pathlib import Path
from sanic import Sanic, response
from sanic.exceptions import SanicException
from nanio.exceptions import NanioException

from .handlers import NodeRPCProxyView, UIView
from .schemas import CoreSettings, RPCSettings, rpc_schemas
from .log import LOGGING_CONFIG_DEFAULTS, Log


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


def settings_from_yaml(_dir, files):
    for file in files:
        path = '{0}/{1}'.format(_dir, file)
        with open(path, 'r') as stream:
            try:
                yield Path(file).stem, yaml_parse(stream)
            except YAMLParseError as err:
                print(str(err))
                raise


class NanioSettings(object):
    def __init__(self, config):
        self.core = CoreSettings(strict=True).load(config['core']).data
        self.rpc = RPCSettings(strict=True).load(config['rpc']).data


class Nanio(Sanic):
    def __init__(self, settings, **kwargs):
        self.cfg = NanioSettings(dict(settings))

        # Set up file synced in-memory shelve
        store_file = self.cfg.core.get('store', env.get('NANIO_STORE_PATH', './.store'))
        self.store = shelve.open(store_file, flag='c')

        self.log_config = LOGGING_CONFIG_DEFAULTS
        self.rpc_nodes = [env.get('NODE_ADDRESS', self.cfg.rpc['nodes'][0])]

        self.rpc_defs = rpc_schemas({
            'public': self.cfg.rpc['actions_public'],
            'protected': self.cfg.rpc['actions_protected'],
        })

        super(Nanio, self).__init__('nanio', **kwargs)


def create_app():
    # Parse config
    directory = env.get('SETTINGS_DIR', 'settings')

    # Create app
    app = Nanio(
        settings=settings_from_yaml(directory, ['core.yml', 'rpc.yml']),
    )

    # Set up logging
    logging.config.dictConfig(app.log_config)
    loglevel = 'DEBUG' if app.cfg.core['debug'] else 'INFO'

    for name in LOGGING_CONFIG_DEFAULTS['loggers'].keys():
        logging.getLogger(name).setLevel(loglevel)

    # Show some useful details
    Log.root.info('Nanio starting...')

    if app.cfg.rpc['enabled']:
        Log.root.info('RPC backends: {0}'.format(','.join(app.rpc_nodes) or 'None configured'))
    else:
        Log.root.info('RPC proxy disabled')

    # Register routes
    app.add_route(NodeRPCProxyView.as_view(app.cfg), '/node-rpc')
    app.add_route(UIView.as_view(), '/api/ui')

    register_error_handlers(app)

    return app
