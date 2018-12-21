# -*- coding: utf-8 -*-

from toastedmarshmallow import Jit
from marshmallow import Schema, fields


class Settings(Schema):
    class Meta:
        jit = Jit


class CoreSettings(Settings):
    listen_host = fields.String(missing='127.0.0.1')
    listen_port = fields.Integer(missing=5000)
    mongodb_host = fields.String(missing='127.0.0.1')
    debug = fields.Bool(missing=False)
    workers = fields.Integer(missing=0)


class RPCSettings(Settings):
    enabled = fields.Bool(missing=False)
    nodes = fields.List(fields.String(), missing=[])
    path = fields.String(missing='/')
    actions_public = fields.List(fields.String(), missing=[])
    actions_protected = fields.List(fields.String(), missing=[])
