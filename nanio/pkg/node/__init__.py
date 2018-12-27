# -*- coding: utf-8 -*-

from jetfactory.base import JetfactoryPackage

from .controllers import NodeController
from .service import NodeService

PKG_NODE = JetfactoryPackage(
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
