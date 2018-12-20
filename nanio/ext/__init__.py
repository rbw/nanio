# -*- coding: utf-8 -*-

from sanic import Blueprint
from .base.service import NanioService
from .node import core_node


class Registry:
    def __init__(self):
        self._blueprints = []
        self.services = {}
        self.base_path = '/api'

    def __getitem__(self, service_name):
        assert service_name in self.services
        return self.services[service_name]

    def init(self, app, motor):
        app.ext = {}
        app.blueprint(Blueprint.group(
            *self._blueprints,
            url_prefix=self.base_path
        ))

        for name, service in self.services.items():
            service.__db__.init(motor[name])
            app.ext[name] = service

    def register(self, blueprint, service, models):
        self._blueprints.append(blueprint)
        self.services[blueprint.name] = service
        service.models_register(models)


registry = Registry()
registry.register(*core_node)
