# -*- coding: utf-8 -*-

from nanio.ext import NanioExtension

from .controllers import NodeController
from .service import NodeService

NODE = NanioExtension(
    name='node',
    controllers=[NodeController],
    service=NodeService,
    documents=[]
)
