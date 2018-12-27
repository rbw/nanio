# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class BaseMeta:
    strict = True
    group = None
    header = None
    desc = None


class Command(Schema):
    class Meta(BaseMeta):
        pass

    action = fields.String(required=True, default='', description='Action name')
