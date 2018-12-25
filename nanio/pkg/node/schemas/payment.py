# -*- coding: utf-8 -*-

from marshmallow import fields
from nanio.config import REQUEST_TIMEOUT
from validation import validate_address, validate_balance, validate_hex

from ._base import Command, BaseMeta


class PaymentCommand(Command):
    wallet = fields.String(required=True, validate=validate_hex)


class PaymentMeta(BaseMeta):
    group = 'Payment'


class PaymentBegin(PaymentCommand):
    class Meta(PaymentMeta):
        name = 'Payment begin'
        action = 'payment_begin'
        description = "Begin a new payment session. Searches wallet for an account that's marked as available and " \
                      "has a 0 balance. If one is found, the account number is returned and is marked as unavailable. " \
                      "If no account is found, a new account is created, placed in the wallet, and returned."
        examples = {
            'request': {
                'action': 'payment_begin',
                'wallet': '000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F'
            },
            'response': {
                "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
            }
        }


class PaymentInit(PaymentCommand):
    class Meta(PaymentMeta):
        name = 'Payment init'
        action = 'payment_init'
        description = "Marks all accounts in wallet as available for being used as a payment session."
        examples = {
            'request': {
              "action": "payment_init",
              "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
            },
            'response': {
                "status": "Ready"
            }
        }


class PaymentEnd(PaymentCommand):
    class Meta(PaymentMeta):
        name = 'Payment end'
        action = 'payment_end'
        description = "End a payment session. Marks the account as available for use in a payment session."
        examples = {
            'request': {
              "action": "payment_end",
              "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
              "wallet": "FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"
            },
            'response': {}
        }

    account = fields.String(required=True, validate=validate_address)


class PaymentWait(PaymentCommand):
    class Meta(PaymentMeta):
        name = 'Payment wait'
        action = 'payment_wait'
        description = "End a payment session. Marks the account as available for use in a payment session."
        examples = {
            'request': {
              "action": "payment_wait",
              "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
              "amount": "1",
              "timeout": "1000"
            },
            'response': "success"
        }

    account = fields.String(required=True, validate=validate_address)
    amount = fields.String(required=True, validate=validate_balance)
    timeout = fields.Integer(required=True, max=REQUEST_TIMEOUT*1000)
