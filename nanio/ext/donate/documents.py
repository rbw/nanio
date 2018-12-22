# -*- coding: utf-8 -*-

from datetime import datetime
from umongo import Document
from umongo.fields import StringField, DateTimeField
from umongo.validate import Length
from nanio.ext.validation import _validate_hex, _validate_address


class Wallet(Document):
    id = StringField(required=True, allow_none=False, validate=_validate_hex)


class DonationPending(Document):
    created = DateTimeField(default=datetime.now())
    message = StringField(required=True, validate=Length(min=1, max=10))
    address = StringField(required=True, allow_none=False, validate=_validate_address)

