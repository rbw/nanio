# -*- coding: utf-8 -*-

from .controllers import NodeController
from .service import NodeService
from nanio.ext import Extension

NODE = Extension(
    name='node',
    controllers=[NodeController],
    service=NodeService,
    documents=[]
)
