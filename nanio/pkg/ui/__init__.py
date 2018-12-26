# -*- coding: utf-8 -*-

from pkg.templates import NanioPackage

from .controllers import UIController
from .service import UIService

PKG_UI = NanioPackage(
    path='/ui',
    controller=UIController,
    service=UIService,
    documents=[],
    meta={
        'name': 'UI',
        'summary': 'Nanio application summary and schemas',
        'description': 'Returns public meta about the Nanio core and registered packages'
    }
)
