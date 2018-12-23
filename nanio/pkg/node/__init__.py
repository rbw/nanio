# -*- coding: utf-8 -*-

from nanio.pkg import NanioPackage

from .controllers import NodeController
from .service import NodeService

NODE = NanioPackage(
    name='node',
    controllers=[NodeController],
    service=NodeService,
    documents=[]
)
