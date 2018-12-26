# -*- coding: utf-8 -*-

from nanio.pkg.templates import NanioPackage

from .controllers import NodeController
from .service import NodeService

PKG_NODE = NanioPackage(
    path='/node',
    controller=NodeController,
    service=NodeService,
    documents=[],
    meta={
        'name': 'Node',
        'summary': 'Node RPC gateway',
        'description': 'Performs various sanity checks before relaying to the Node RPC server'
    }
)
