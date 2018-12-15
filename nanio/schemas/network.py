# -*- coding: utf-8 -*-

from marshmallow import fields

from ._base import Action, BaseMeta
from ._validation import _validate_hex


class NetworkMeta(BaseMeta):
    group = 'Network'


class AvailableSupply(Action):
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


class Representatives(Action):
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


class RepresentativesOnline(Action):
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


class Republish(Action):
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

    hash = fields.String(required=True, default='', validate=_validate_hex)

