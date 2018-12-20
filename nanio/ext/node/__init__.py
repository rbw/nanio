# -*- coding: utf-8 -*-

from .controller import bp
from .service import NodeService
from .models import Test

core_node = (bp, NodeService(), [Test])
