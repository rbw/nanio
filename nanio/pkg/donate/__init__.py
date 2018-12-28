# -*- coding: utf-8 -*-

from jetfactory.base import JetfactoryPackage

from .controllers import DonationController
from .service import DonationService
from .documents import Wallet, Donation


pkg_donate = JetfactoryPackage(
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
