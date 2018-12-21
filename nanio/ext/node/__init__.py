# -*- coding: utf-8 -*-

from .controller import NodeController
from .service import NodeService
from nanio.ext import Extension

EXTENSION__NODE = Extension(
    name='node',
    controllers=[NodeController],
    service=NodeService(),
    documents=[]
)
