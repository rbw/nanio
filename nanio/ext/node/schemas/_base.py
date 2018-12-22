# -*- coding: utf-8 -*-

from toastedmarshmallow import Jit
from marshmallow import Schema, fields


class BaseMeta:
    jit = Jit
    strict = True
    group = None
    header = None
    desc = None


class Command(Schema):
    class Meta(BaseMeta):
        pass

    action = fields.String(required=True, default='', description='Action name')
