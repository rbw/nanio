# -*- coding: utf-8 -*-

from jetfactory.base import JetfactoryPackage

from .controllers import UIController
from .service import UIService

pkg_ui = JetfactoryPackage(
    controller=UIController,
    service=UIService,
    meta={
        'name': 'UI',
        'summary': 'Jetfactory application summary and schemas',
        'description': 'Returns public meta about the Jetfactory core and registered packages'
    }
)
