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

from .network import AvailableSupply, Representatives, RepresentativesOnline, Republish
from .node import Version

RPC_SCHEMAS = [
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


