# -*- coding: utf-8 -*-

from datetime import datetime
from umongo import Document
from umongo.fields import StringField, DateTimeField, BooleanField
from umongo.validate import Length
from nanio.ext.validation import validate_hex, validate_address, validate_ip


class Wallet(Document):
    wallet_id = StringField(required=True, allow_none=False, validate=validate_hex)
    created_on = DateTimeField(default=datetime.now)


class Donation(Document):
    message = StringField(required=True, validate=Length(min=1, max=10))
    address_from = StringField(required=True, allow_none=False, validate=validate_address)
    address_to = StringField(required=True, allow_none=False, validate=validate_address)
    created_on = DateTimeField(default=datetime.now)
    origin_addr = StringField(required=True, allow_none=False, validate=validate_ip)
    pending = BooleanField(required=True, default=True)
