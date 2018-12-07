# -*- coding: utf-8 -*-

from ._base import Action, BaseMeta


class NodeMeta(BaseMeta):
    group = 'Node'


class Version(Action):
    class Meta(NodeMeta):
        name = 'Retrieve node versions'
        action = 'version'
        description = 'Returns version information for RPC, Store, Protocol (network) & Node (Major & Minor version) ' \
                      'RPC Version always retruns "1" as of 01/11/2018'
        examples = {
            'request': {
              "action": "version"
            },
            'response': {
              "rpc_version": "1",
              "store_version": "11",
              "protocol_version": "15",
              "node_vendor": "RaiBlocks 17.0"
            }
        }
