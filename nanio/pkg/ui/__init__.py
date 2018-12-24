# -*- coding: utf-8 -*-

from nanio.pkg import NanioPackage

from .controllers import UIController
from .service import UIService


UI = NanioPackage(
    name='ui',
    controllers=[UIController],
    service=UIService,
    documents=[]
)
