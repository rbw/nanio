# -*- coding: utf-8 -*-

from marshmallow import fields, Schema
from jetfactory.utils import yaml_parse
from jetfactory.base import PackageSettings


class Commands(Schema):
    public = fields.List(fields.String(), missing=[])
    protected = fields.List(fields.String(), missing=[])
    private = fields.List(fields.String(), missing=[])


class Settings(PackageSettings):
    enabled = fields.Bool(missing=False)
    nodes = fields.List(fields.String(), missing=[])
    commands = fields.Nested(Commands, required=True)


settings = (Settings, yaml_parse('node.yml'))
