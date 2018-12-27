# -*- coding: utf-8 -*-

from marshmallow import fields
from nanio.validation import validate_hex

from ._base import Command, BaseMeta


class NetworkMeta(BaseMeta):
    group = 'Network'


class AvailableSupply(Command):
    class Meta(NetworkMeta):
        name = 'Available supply'
        action = 'available_supply'
        description = 'Returns how many rai are in the public supply'
        examples = {
            'request': {
                'action': 'available_supply'
            },
            'response': {
                'available': '10000'
            }
        }


class Representatives(Command):
    class Meta(NetworkMeta):
        name = 'Representatives'
        action = 'representatives'
        description = 'Returns a list of pairs of representative and its voting weight'
        examples = {
            'request': {
                "action": "representatives",
                "sorting": True,
                "count": 50,
            },
        }

    count = fields.Integer(required=False, missing=20, default=50)
    sorting = fields.Boolean(required=False, default=True)


class RepresentativesOnline(Command):
    class Meta(NetworkMeta):
        name = 'Representatives online'
        action = 'representatives_online'
        description = 'Returns a list of pairs of online representative accounts that have voted ' \
                      'recently and empty strings'
        examples = {
            'request': {
              "action": "representatives_online"
            },
        }


class Republish(Command):
    class Meta(NetworkMeta):
        name = 'Republish'
        action = 'republish'
        description = 'Rebroadcast blocks starting at hash to the network'
        examples = {
            'request': {
              "action": "republish",
              "hash": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
            },
        }

    hash = fields.String(required=True, default='', validate=validate_hex)

