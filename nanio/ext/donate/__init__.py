# -*- coding: utf-8 -*-

from .controllers import DonateController
from .service import DonateService
from .documents import Wallet
from nanio.ext import Extension

DONATE = Extension(
    name='donate',
    controllers=[DonateController],
    service=DonateService,
    documents=[Wallet]
)
