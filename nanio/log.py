# -*- coding: utf-8 -*-

import logging
import sys


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'nanio.api': {
            'level': 'DEBUG',
            'handlers': ['api_console'],
            'propagate': True,
            'qualname': 'nanio.api'
        },
        'sanic.error': {
            'level': 'INFO',
            'handlers': ['error_console'],
            'propagate': True,
            'qualname': 'sanic.error'
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stdout
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stderr
        },
        'api_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'api_access',
            'stream': sys.stdout
        },
    },
    formatters={
        'api_access': {
            # 'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(name)s %(remote_addr)s] %(message)s',
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter'
        },
        'generic': {
            'format': '[%(levelname)1.1s %(asctime)s.%(msecs)03d %(process)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'class': 'logging.Formatter'
        },
    }
)


log_root = logging.getLogger('root')
