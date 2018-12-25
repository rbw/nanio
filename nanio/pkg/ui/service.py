# -*- coding: utf-8 -*-

from pkg.templates import NanioService


class UIService(NanioService):
    def __init__(self, *args, **kwargs):
        super(UIService, self).__init__(*args, **kwargs)
        self.node_schemas = self.pkgs.node.svc.schemas.by_category
        self.routes = self.app.router.routes_names

    async def get_schemas(self):
        for name, pkg in self.pkgs:
            if pkg.name in ['node', 'ui']:
                continue

            for ctrl in pkg.controllers:
                name = ctrl.__name__
                path, route = self.routes[name]

        return {}
        """return dict(
            node=self.node_schemas
        )"""
