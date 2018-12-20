# -*- coding: utf-8 -*-

from umongo import Document
from umongo.fields import StringField


class Test(Document):
    test = StringField(required=True, allow_none=False)
