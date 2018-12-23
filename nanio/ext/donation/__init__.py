# -*- coding: utf-8 -*-

from nanio.ext import NanioExtension

from .controllers import DonationController
from .service import DonationService
from .documents import Wallet, Donation


DONATION = NanioExtension(
    name='donations',
    controllers=[DonationController],
    service=DonationService,
    documents=[Wallet, Donation]
)
