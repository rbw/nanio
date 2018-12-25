# -*- coding: utf-8 -*-

from toastedmarshmallow import Jit
from marshmallow import Schema, fields


class BaseMeta:
    jit = Jit
    strict = True


class NanioSchema(Schema):
    class Meta(BaseMeta):
        pass
