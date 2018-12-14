# -*- coding: utf-8 -*-

import logging
import sys


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "root": {
            "level": "DEBUG",
            "handlers": ["console"]
        },
        "nanio.node_rpc": {
            "level": "DEBUG",
            "handlers": ["access_console"],
            "qualname": "nanio.node_rpc"
        },
        "sanic.error": {
            "level": "DEBUG",
            "handlers": ["error_console"],
            "qualname": "sanic.error"
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
    },
    formatters={
        "generic": {
            "format": '[%(levelname)1.1s %(asctime)s] %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter"
        },
        "access": {
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(host)s] %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter"
        },
    }
)


class Log:
    root = logging.getLogger('root')
    node_rpc = logging.getLogger('nanio.node_rpc')
    error = logging.getLogger('sanic.error')
