# -*- coding: utf-8 -*-

from jetfactory.base import JetPackage

from .controller import DonationController
from .service import DonationService
from .model import Wallet, Donation


pkg_donate = JetPackage(
    controller=DonationController,
    service=DonationService,
    documents=[Wallet, Donation],
    meta={
        'name': 'nanio-donate',
        'summary': 'Package for sending and listing donations',
        'description': 'Keeps track of donations, uses Github OAuth2'
    }
)
