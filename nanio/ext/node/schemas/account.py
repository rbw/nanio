# -*- coding: utf-8 -*-

from marshmallow import fields
from nanio.ext.validation import validate_address, validate_balance, validate_hex

from ._base import Command, BaseMeta


class AccountMeta(BaseMeta):
    group = 'Account'


class Account(Command):
    class Meta(AccountMeta):
        pass

    account = fields.String(required=True, validate=validate_address, description='Address ("xrb_1ipx8...")')


class Accounts(Command):
    class Meta(AccountMeta):
        pass

    accounts = fields.List(
        fields.String(
            validate=validate_address,
            required=True
        ),
        required=True,
       
        description='Addresses (["xrb_1ipx8..", "xrb_1ipx8..", ..])'
    )


class AccountsPending(Accounts):
    class Meta(AccountMeta):
        name = 'Accounts pending'
        action = 'accounts_pending'
        description = 'Returns a list of block hashes which have not yet been received by these accounts'
        examples = {
            'request': {
              "action": "accounts_pending",
              "accounts": ["xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou", "xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4"],
              "count": 1
            },
        }

    source = fields.Boolean(required=False, default=False)
    include_active = fields.Boolean(required=False, default=False)
    count = fields.Integer(required=False, default=False)
    threshold = fields.Integer(required=False, validate=validate_balance)


class AccountsBalances(Accounts):
    class Meta(AccountMeta):
        name = 'Accounts balances'
        action = 'validate_account_number'
        description = 'Returns how many RAW is owned and how many have not yet been received by accounts list'
        examples = {
            'request': {
              "action": "accounts_balances",
              "accounts": ["xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou", "xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4"]
            },
        }


class AccountValidate(Account):
    class Meta(AccountMeta):
        name = 'Validate account'
        action = 'validate_account_number'
        description = 'Check whether account is a valid account number'
        examples = {
            'request': {
              "action": "validate_account_number",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class AccountKey(Account):
    class Meta(AccountMeta):
        name = 'Account public key'
        action = 'account_key'
        description = 'Get the public key for account'
        examples = {
            'request': {
              "action": "account_key",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class AccountBalance(Account):
    class Meta(AccountMeta):
        name = 'Account balance'
        action = 'account_balance'
        description = 'Returns how many RAW is owned and how many have not yet been received by account'
        examples = {
            'request': {
              "action": "account_balance",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class AccountBlockCount(Account):
    class Meta(AccountMeta):
        name = 'Account block count'
        action = 'account_block_count'
        description = 'Get number of blocks for a specific account'
        examples = {
            'request': {
              "action": "account_block_count",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class AccountWeight(Account):
    class Meta(AccountMeta):
        name = 'Account weight'
        action = 'account_weight'
        description = 'Returns the voting weight for account'
        examples = {
            'request': {
              "action": "account_weight",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class AccountRepresentative(Account):
    class Meta(AccountMeta):
        name = 'Account representative'
        action = 'account_representative'
        description = 'Returns the representative for account'
        examples = {
            'request': {
              "action": "account_representative",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class Delegators(Account):
    class Meta(AccountMeta):
        name = 'Delegators'
        action = 'delegators'
        description = 'Returns a list of pairs of delegator names given account a representative and its balance'
        examples = {
            'request': {
              "action": "delegators",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }


class DelegatorsCount(Account):
    class Meta(AccountMeta):
        name = 'Delegators count'
        action = 'delegators_count'
        description = 'Get number of delegators for a specific representative account'
        examples = {
            'request': {
              "action": "delegators_count",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
            'response': {
               "count": "2"
            }
        }


class AccountInfo(Account):
    class Meta(AccountMeta):
        name = 'Account information'
        action = 'account_info'
        description = 'Returns frontier, open block, change representative block, balance, last modified timestamp ' \
                      'from local database & block count for account. Only works for accounts that have an entry on ' \
                      'the ledger, will return "Account not found" otherwise.'
        examples = {
            'request': {
              "action": "account_info",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
            },
        }

    representative = fields.Boolean(required=False, default=False)
    weight = fields.Boolean(required=False, default=False)
    pending = fields.Boolean(required=False, default=False)


class AccountHistory(Account):
    class Meta(AccountMeta):
        name = 'Account history'
        action = 'account_history'
        description = 'Reports send/receive information for an account. Change blocks are skipped, ' \
                      'open blocks will appear as receive (unless raw is set to true - see optional parameters ' \
                      'below). Response will start with the latest block for the account (the frontier), ' \
                      'and will list all blocks back to the open block of this account when "count" is set to "-1".'
        examples = {
            'request': {
              "action": "account_history",
              "account": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
              "count": "1"
            },
        }

    count = fields.Integer(required=False, default=-1)
    raw = fields.Boolean(required=False, default=False)
    head = fields.String(required=False, validate=validate_hex)


class AccountsFrontiers(Accounts):
    class Meta(AccountMeta):
        name = 'Accounts frontiers'
        action = 'accounts_frontiers'
        description = 'Returns a list of pairs of account and block hash representing the head block for accounts list'
        examples = {
            'request': {
              "action": "accounts_frontiers",
              "accounts": ["xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou", "xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4"]
            },
        }
