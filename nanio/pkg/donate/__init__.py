# -*- coding: utf-8 -*-

from nanio.pkg import NanioPackage

from .controllers import DonationController
from .service import DonationService
from .documents import Wallet, Donation


DONATE = NanioPackage(
    name='donations',
    controllers=[DonationController],
    service=DonationService,
    documents=[Wallet, Donation]
)
