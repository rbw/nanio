# -*- coding: utf-8 -*-

from jetfactory.base import JetService


class UIService(JetService):
    async def get_schemas(self, node_schemas):
        routes = self.app.router.routes_names

        for name, pkg in self.app.pkgs:
            if pkg.name in ['node', 'ui']:
                continue

            for ctrl in pkg.controllers:
                name = ctrl.__name__
                path, route = routes[name]

        return {}
