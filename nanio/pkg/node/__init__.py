# -*- coding: utf-8 -*-

from jetfactory.base import JetPackage

from .controller import NodeController
from .service import NodeService
from .settings import settings

pkg_node = JetPackage(
    controller=NodeController,
    service=NodeService,
    settings=settings,
    meta={
        'name': 'nanio-node',
        'summary': 'Node RPC gateway',
        'description': 'Performs various sanity checks before relaying to the Node RPC server'
    }
)
