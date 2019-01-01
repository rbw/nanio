# -*- coding: utf-8 -*-

from jetfactory.base import JetPackage

from .controller import UIController
from .service import UIService

pkg_ui = JetPackage(
    controller=UIController,
    service=UIService,
    meta={
        'name': 'nanio-ui',
        'summary': 'Jetfactory application summary and schemas',
        'description': 'Returns public meta about the Jetfactory core and registered packages'
    }
)
