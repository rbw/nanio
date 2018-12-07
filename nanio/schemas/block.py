# -*- coding: utf-8 -*-

import ujson
from marshmallow import fields, Schema, pre_load, post_dump, ValidationError

from ._base import Action, BaseMeta

from ._validation import (
    _validate_address, _validate_balance,
    _validate_hex, _validate_link,
    _validate_previous, _validate_type
)


class BlockMeta(BaseMeta):
    group = 'Block'


class StateBlock(Schema):
    type = fields.String(required=True, validate=_validate_type)
    account = fields.String(required=True, validate=_validate_address)
    previous = fields.String(required=True, validate=_validate_previous)
    representative = fields.String(required=False, validate=_validate_address)
    balance = fields.String(required=True, validate=_validate_balance)
    link = fields.String(required=True, validate=_validate_link)
    signature = fields.String(required=True, validate=_validate_hex)
    work = fields.String(required=True, validate=_validate_hex)


class BlockAction(Action):
    class Meta(BlockMeta):
        pass

    block = fields.String(required=True, validate=_validate_hex)


class HashBlock(Action):
    class Meta(BlockMeta):
        pass

    hash = fields.String(required=True, validate=_validate_hex)


class HashesBlock(Action):
    class Meta(BlockMeta):
        pass

    hashes = fields.List(
        fields.String(
            validate=_validate_hex,
            required=True
        ),
        required=True,
       
        description='Hashes (["6CDDA486..", "9FAAD64..", ..])'
    )


class Process(Action):
    class Meta(BlockMeta):
        name = 'Process block'
        action = 'process'
        description = 'Publish block to the network'
        examples = {
            'request': {  
                "action": "process",
                "block": {
                    "type": "state",
                    "account": "xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
                    "previous": "6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766",
                    "representative": "xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh",
                    "balance": "40200000001000000000000000000000000",
                    "link": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
                    "link_as_account": "xrb_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd",
                    "signature": "A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07",
                    "work": "000bc55b014e807d"
                }
            }
        }

    block = fields.Nested(StateBlock, required=True)

    @pre_load
    def _loads(self, data):
        if 'block' in data:
            try:
                data['block'] = ujson.loads(data['block'])
            except (ValueError, TypeError):
                raise ValidationError('Invalid block format')
        else:
            raise ValidationError('Missing block contents')

        return data

    @post_dump
    def _dumps(self, data):
        data['block'] = ujson.dumps(data['block'])
        return data


class BlockCountType(Action):
    class Meta(BlockMeta):
        name = 'Block count by type'
        action = 'block_count_type'
        description = 'Reports the number of blocks in the ledger by type (send, receive, open, change, state)'
        examples = {
            'request': {
              "action": "block_count_type"
            },
        }


class BlockCount(Action):
    class Meta(BlockMeta):
        name = 'Block count'
        action = 'block_count'
        description = 'Reports the number of blocks in the ledger and unchecked synchronizing blocks'
        examples = {
            'request': {
              "action": "block_count"
            },
        }


class BlockConfirm(HashBlock):
    class Meta(BlockMeta):
        name = 'Block confirm'
        action = 'block_confirm'
        description = 'Request confirmation for block from known online representative nodes. ' \
                      'Check results with Confirmation history'
        examples = {
            'request': {
              "action": "block_confirm",
              "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"
            },
        }


class Block(HashBlock):
    class Meta(BlockMeta):
        name = 'Retrieve block'
        action = 'block'
        description = 'Retrieves a json representation of block'
        examples = {
            'request': {
              "action": "block",
              "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"
            },
        }


class PendingExists(HashBlock):
    class Meta(BlockMeta):
        name = 'Pending exists'
        action = 'pending_exists'
        description = 'Check whether block is pending by hash'
        examples = {
            'request': {
              "action": "pending_exists",
              "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"
            },
            'response': {
              "exists": "1"
            }
        }


class Blocks(HashesBlock):
    class Meta(BlockMeta):
        name = 'Multiple blocks'
        action = 'blocks'
        description = 'Retrieves a json representations of blocks'
        examples = {
            'request': {
              "action": "blocks",
              "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]
            },
        }


class BlocksInfo(HashesBlock):
    class Meta(BlockMeta):
        name = 'Multiple blocks with amount'
        action = 'blocks_info'
        description = 'Retrieves a json representations of blocks with transaction amount & block account Request'
        examples = {
            'request': {
              "action": "blocks_info",
              "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]
            },
        }

    pending = fields.Bool(required=False, default=False)
    source = fields.Bool(required=False, default=False)
    balance = fields.Bool(required=False, default=False)


class BlockHash(Process):
    class Meta(BlockMeta):
        name = 'Block hash'
        action = 'block_hash'
        description = 'Returning block hash for given block content'
        examples = {
            'request': {  
              "action": "block_hash",     
              "block": {
                  "type": "state",    
                  "account": "xrb_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr",    
                  "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",    
                  "representative": "xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",    
                  "balance": "1000000000000000000000",    
                  "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",    
                  "link_as_account": "xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",    
                  "signature": "3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A",    
                  "work": "cab7404f0b5449d0"
               }
            },
        }


class BlockAccount(HashBlock):
    class Meta(BlockMeta):
        name = 'Block account'
        action = 'block_account'
        description = 'Returns the account containing block'
        examples = {
            'request': {
              "action": "block_account",
              "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"
            },
        }


class Successors(BlockAction):
    class Meta(BlockMeta):
        name = 'Successors'
        action = 'successors'
        description = 'Returns a list of block hashes in the account chain ending at block up to count'
        examples = {
            'request': {
              "action": "successors",
              "block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
              "count": "1"
            },
        }


class Chain(BlockAction):
    class Meta(BlockMeta):
        name = 'Chain'
        action = 'chain'
        description = 'Returns a consecutive list of block hashes in the account chain starting at block up to ' \
                      'count. Will list all blocks back to the open block of this chain when count is set to "-1".' \
                      'The requested block hash is included in the answer.'
        examples = {
            'request': {
              "action": "chain",
              "block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
              "count": "1"
            },
        }

    block = fields.String(required=True, validate=_validate_hex)
    count = fields.Integer(required=False, default=-1)
