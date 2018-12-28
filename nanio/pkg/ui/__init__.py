# -*- coding: utf-8 -*-

from jetfactory.base import JetfactoryPackage

from .controllers import UIController
from .service import UIService

PKG_UI = JetfactoryPackage(
    path='/ui',
    controller=UIController,
    service=UIService,
    documents=[],
    meta={
        'name': 'UI',
        'summary': 'Jetfactory application summary and schemas',
        'description': 'Returns public meta about the Jetfactory core and registered packages'
    }
)
