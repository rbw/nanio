# -*- coding: utf-8 -*-

from .controller import bp
from .service import NodeService

core_node = (bp, NodeService(), )
