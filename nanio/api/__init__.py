# -*- coding: utf-8 -*-

from sanic import Blueprint
from .nano import gateway, schemas

base = Blueprint.group(
    schemas,
    url_prefix='/api'
)
