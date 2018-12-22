# -*- coding: utf-8 -*-

from toastedmarshmallow import Jit
from marshmallow import Schema, fields


class Settings(Schema):
    class Meta:
        jit = Jit


class Commands(Settings):
    public = fields.List(fields.String(), missing=[])
    protected = fields.List(fields.String(), missing=[])
    private = fields.List(fields.String(), missing=[])


class SettingsCore(Settings):
    listen_host = fields.String(missing='127.0.0.1')
    listen_port = fields.Integer(missing=5000)
    mongodb_host = fields.String(missing='127.0.0.1')
    mongodb_port = fields.String(missing=27017)
    debug = fields.Bool(missing=False)
    workers = fields.Integer(missing=0)


class SettingsRPC(Settings):
    enabled = fields.Bool(missing=False)
    nodes = fields.List(fields.String(), missing=[])
    commands = fields.Nested(Commands, required=True)
