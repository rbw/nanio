# -*- coding: utf-8 -*-

from nanio.pkg.templates import NanioPackage

from .controllers import NodeController
from .service import NodeService

NODE = NanioPackage(
    path='/node',
    controllers=[NodeController],
    service=NodeService,
    documents=[],
    meta={
        'name': 'Node',
        'summary': 'Node RPC gateway',
        'description': 'Performs various sanity checks before relaying to the Node RPC server'
    }
)
