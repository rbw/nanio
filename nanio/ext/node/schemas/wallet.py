# -*- coding: utf-8 -*-

from marshmallow import fields
from nanio.ext.validation import _validate_hex

from ._base import Command, BaseMeta


class WalletCommand(Command):
    wallet = fields.String(required=True, validate=_validate_hex)


class WalletMeta(BaseMeta):
    group = 'Wallet'


class WalletCreate(Command):
    class Meta(WalletMeta):
        name = 'Wallet create'
        action = 'wallet_create'
        description = 'Creates a new random wallet id'
        examples = {
            'request': {
              'action': 'wallet_create'
            },
            'response': {
                'wallet': '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F'
            }
        }


class WalletFrontiers(WalletCommand):
    class Meta(WalletMeta):
        name = 'Wallet frontiers'
        action = 'wallet_frontiers'
        description = 'Returns a list of pairs of account and block hash representing the head block starting ' \
                      'for accounts from wallet'
        examples = {
            'request': {
              'action': 'wallet_frontiers',
              'wallet': '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F'
            },
            'response': {
                'frontiers': {
                    'xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000':
                        '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F'
                }
            }
        }


class WalletInfo(WalletCommand):
    class Meta(WalletMeta):
        name = 'Wallet info'
        action = 'wallet_info'
        description = 'Returns a list of pairs of account and block hash representing the head block starting ' \
                      'for accounts from wallet'
        examples = {
            'request': {
              'action': 'wallet_info',
              'wallet': '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F'
            },
            'response': {
              "balance": "10000",
              "pending": "10000",
              "accounts_count": "3",
              "adhoc_count": "1",
              "deterministic_count": "2",
              "deterministic_index": "2"
            }
        }

