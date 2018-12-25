# -*- coding: utf-8 -*-

from toastedmarshmallow import Jit
from marshmallow import Schema, fields
from nanio.validation import validate_alphanum


class PackageMeta(Schema):
    class Meta:
        jit = Jit

    name = fields.String(required=True, validate=validate_alphanum)
    summary = fields.String(required=True)
    description = fields.String(required=True)


class NanioPackage:
    def __init__(self, path, controllers, service, documents, meta):
        self.meta = PackageMeta(strict=True).load(meta).data
        self.name = self.meta['name'].lower()
        self.path = path
        self.svc = service
        self.collection = 'nanio__'.format(self.name)
        self.controllers = controllers
        self.documents = documents

    def __repr__(self):
        return '<NanioPackage [{0}] at {1}>'.format(self.name, hex(id(self)))
