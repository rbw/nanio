# -*- coding: utf-8 -*-

from sanic import Blueprint
from .node import gateway, schemas

base = Blueprint.group(
    schemas,
    url_prefix='/api'
)
