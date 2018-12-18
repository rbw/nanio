# -*- coding: utf-8 -*-

from .block import (
    Process, Block, Blocks, Chain, BlockCount, BlockCountType,
    BlockConfirm, BlockAccount, Successors, BlocksInfo,
    BlockHash, PendingExists
)

from .account import (
    AccountsPending, AccountHistory, Delegators,
    DelegatorsCount, AccountInfo, AccountsFrontiers,
    AccountValidate, AccountsBalances, AccountBalance,
    AccountBlockCount, AccountWeight, AccountRepresentative,
    AccountKey,
)

from .config import CoreSettings, RPCSettings
from .network import AvailableSupply, Representatives, RepresentativesOnline, Republish
from .node import Version

SCHEMAS = [
    # Network
    AvailableSupply(), Representatives(), RepresentativesOnline(), Republish(),

    # Node
    Version(),

    # Account
    AccountKey(), AccountBalance(), AccountBlockCount(), AccountWeight(),
    AccountInfo(), AccountHistory(), AccountRepresentative(), AccountsBalances(),
    AccountsPending(), AccountsFrontiers(), Delegators(), DelegatorsCount(),

    # Block
    Process(), Chain(), Block(), AccountValidate(), BlockConfirm(), BlockAccount(),
    BlocksInfo(), BlockCount(), BlockCountType(), Blocks(), Successors(), BlockHash(),
    PendingExists(),
]

ACTIONS_SCHEMAS = {s.Meta.action: s for s in SCHEMAS}


def get_rpc_schema(actions_enabled):
    groups = {}

    for _, schema in sorted(ACTIONS_SCHEMAS.items()):
        group = schema.Meta.group
        action = schema.Meta.action

        action = {
            'name': schema.Meta.name,
            'action': action,
            'description': schema.Meta.description,
            'enabled': action in actions_enabled['public'] + actions_enabled['protected'],
            'protected': action in actions_enabled['protected'],
            'examples': schema.Meta.examples,
            'fields': []
        }

        for name, field in schema._declared_fields.items():
            action['fields'].append({
                'name': name,
                'required': field.required,
                'type': field.__class__.__name__,
                'description': field.metadata.get('description', None)
            })

        if group not in groups:
            groups[group] = []

        groups[group].append(action)

    return groups
