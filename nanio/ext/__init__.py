# -*- coding: utf-8 -*-

from sanic import Blueprint
from .common import NanioService
from .node import core_node


class Registry:
    def __init__(self):
        self._blueprints = []
        self.services = {}
        self.base_path = '/api'

    def __getitem__(self, service_name):
        assert service_name in self.services
        return self.services[service_name]

    def register(self, blueprint, service=None):
        self._blueprints.append(blueprint)
        self.services[blueprint.name] = service

    @property
    def blueprints(self):
        return Blueprint.group(
            *self._blueprints,
            url_prefix=self.base_path
        )


registry = Registry()
registry.register(*core_node)
