# -*- coding: utf-8 -*-

from marshmallow import fields, Schema
from jetfactory.utils import yaml_parse


class Commands(Schema):
    public = fields.List(fields.String(), missing=[])
    protected = fields.List(fields.String(), missing=[])
    private = fields.List(fields.String(), missing=[])


class Settings(Schema):
    enabled = fields.Bool(missing=False)
    nodes = fields.List(fields.String(), missing=[])
    commands = fields.Nested(Commands, required=True)


_contents = dict(yaml_parse('node.yml'))
settings = Settings(strict=True).load(_contents).data
