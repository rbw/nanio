# -*- coding: utf-8 -*-

from marshmallow import fields

from nanio.validation import validate_balance
from ._base import Command, BaseMeta


class ConversionCommand(Command):
    amount = fields.String(required=True, validate=validate_balance, description='Amount to convert')


class ConversionMeta(BaseMeta):
    group = 'Conversion'


class MraiFromRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Mrai from raw'
        action = 'mrai_from_raw'
        description = 'Divide a raw amount down by the Mrai ratio.'
        examples = {
            'request': {
              'action': 'mrai_from_raw',
              'amount': '1000000000000000000000000000000'
            },
            'response': {
                'amount': '1'
            }
        }


class MraiToRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Mrai to raw'
        action = 'mrai_to_raw'
        description = 'Multiply an Mrai amount by the Mrai ratio.'
        examples = {
            'request': {
              'action': 'mrai_to_raw',
              'amount': '1'
            },
            'response': {
                'amount': '1000000000000000000000000000000'
            }
        }


class KraiFromRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Krai from raw'
        action = 'krai_from_raw'
        description = 'Divide a raw amount down by the krai ratio.'
        examples = {
            'request': {
              'action': 'krai_from_raw',
              'amount': '1000000000000000000000000000'
            },
            'response': {
                'amount': '1'
            }
        }


class KraiToRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Krai to raw'
        action = 'krai_to_raw'
        description = 'Multiply an krai amount by the krai ratio.'
        examples = {
            'request': {
              'action': 'krai_to_raw',
              'amount': '1'
            },
            'response': {
                'amount': '1000000000000000000000000000'
            }
        }


class RaiFromRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Rai from raw'
        action = 'rai_from_raw'
        description = 'Divide a raw amount down by the rai ratio.'
        examples = {
            'request': {
              'action': 'rai_from_raw',
              'amount': '1000000000000000000000000'
            },
            'response': {
                'amount': '1'
            }
        }


class RaiToRaw(ConversionCommand):
    class Meta(ConversionMeta):
        name = 'Rai to raw'
        action = 'rai_to_raw'
        description = 'Multiply an rai amount by the rai ratio.'
        examples = {
            'request': {
              'action': 'rai_to_raw',
              'amount': '1'
            },
            'response': {
                'amount': '1000000000000000000000000'
            }
        }
