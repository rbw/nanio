# -*- coding: utf-8 -*-

from nanio.pkg import NanioService


class UIService(NanioService):
    def __init__(self, *args, **kwargs):
        super(UIService, self).__init__(*args, **kwargs)
        self.node = self.pkg.node.svc

    async def node_schemas(self):
        return self.node.schemas.by_category

    @property
    async def schemas(self):
        return dict(
            node=await self.node_schemas()
        )
