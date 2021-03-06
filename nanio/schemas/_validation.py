# -*- coding: utf-8 -*-

import libn
import decimal
from marshmallow import ValidationError

# Validation error messages
INVALID_HEX = 'must be valid hex'
INVALID_BALANCE = 'must be in raw format'
INVALID_LINK = [
    "Open/Receive -> must equal pairing send block's hash",
    "Change -> must equal 0",
    "Send -> must equal destination xrb_ or nano_ address"
]
INVALID_PREVIOUS = 'must be 0 if open block, or previous head block on account (hex)'
INVALID_ADDRESS = 'must be a valid address prefixed with xrb_ or nano_'
INVALID_TYPE = 'must be state'


def _validate_hex(value):
    try:
        bytes.fromhex(value)
    except ValueError:
        raise ValidationError(INVALID_HEX)


def _validate_balance(value):
    try:
        libn.rai_from_raw(value)
    except decimal.InvalidOperation:
        raise ValidationError(INVALID_BALANCE)


def _validate_link(value):
    try:
        bytes.fromhex(value)
    except ValueError:
        try:
            if str(int(value)) == '0':
                pass
            elif libn.validate_account_number(value):
                pass
            else:
                raise
        except ValueError:
            raise ValidationError(INVALID_LINK)


def _validate_previous(value):
    try:
        bytes.fromhex(value)
    except ValueError:
        try:
            if str(int(value)) != '0':
                raise
        except ValueError:
            raise ValidationError(INVALID_PREVIOUS)


def _validate_address(value):
    try:
        libn.validate_account_number(value)
    except Exception:
        raise ValidationError(INVALID_ADDRESS)


def _validate_type(value):
    if value != 'state':
        raise ValidationError(INVALID_TYPE)

