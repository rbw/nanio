# -*- coding: utf-8 -*-

from pkg.templates import NanioPackage

from .controllers import DonationController
from .service import DonationService
from .documents import Wallet, Donation


PKG_DONATE = NanioPackage(
    path='/donations',
    controller=DonationController,
    service=DonationService,
    documents=[Wallet, Donation],
    meta={
        'name': 'Donate',
        'summary': 'Package for sending and listing donations',
        'description': 'Keeps track of donations, uses Github OAuth2'
    }
)