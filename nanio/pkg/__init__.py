# -*- coding: utf-8 -*-

from enum import Enum
from collections import namedtuple

Route = namedtuple('NanioRoute', ['handler', 'path', 'method'])


class Methods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
