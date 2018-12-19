# -*- coding: utf-8 -*-

import functools
import ujson

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.http_exceptions import HttpProcessingError
from marshmallow import ValidationError

from nanio.exceptions import NanioException
from nanio.schemas import ACTIONS_SCHEMAS
from nanio.config import (
    RPC_NODES, RPC_ENABLED,
    RPC_ACTIONS_PUBLIC, RPC_ACTIONS_PROTECTED,
)

from ._base import Service


class NanoService(Service):
    def __init__(self):
        self.rpc_url = RPC_NODES[0]
        self.rpc_schemas = self.get_rpc_schemas()

    async def get_rpc_schemas(self):
        self.log.info('GET RPC schemas')

        groups = {}

        for _, schema in sorted(ACTIONS_SCHEMAS.items()):
            group = schema.Meta.group
            action = schema.Meta.action

            action = {
                'name': schema.Meta.name,
                'action': action,
                'description': schema.Meta.description,
                'enabled': action in RPC_ACTIONS_PUBLIC + RPC_ACTIONS_PROTECTED,
                'protected': action in RPC_ACTIONS_PROTECTED,
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

    async def validate_body(self, body):
        if not body or 'action' not in body:
            raise NanioException('Missing action in payload', 400)

        action = body['action']
        schema = ACTIONS_SCHEMAS.get(action, None)

        if not schema:
            raise NanioException('Unknown action', 422)
        elif action not in RPC_ACTIONS_PUBLIC:
            raise NanioException('Disabled action', 422)
        elif action in RPC_ACTIONS_PROTECTED:
            print('PROTECTED! -- add auth')

        try:
            validated = schema.load(body).data
        except ValidationError as err:
            get_errors = functools.partial(ujson.dumps, err.messages)

            if self.debug:
                self.log.debug('Validation failed:\n{0}'.format(get_errors(indent=4)))
            else:
                self.log.warning('Payload validation failed (action: {0})'.format(action))

            raise NanioException(get_errors(), 422)

        return schema.dumps(validated).data

    async def send(self, body):
        if not RPC_ENABLED:
            return {'result': 'RPC proxy disabled'}, 200

        payload = await self.validate_body(body)

        if self.debug:
            self.log.debug('Send [{0}]:\n{1}'.format(body['action'], payload))
        else:
            self.log.info('Send [{0}]'.format(payload['action']))

        try:
            status, result = self.http_post(payload)

            if self.debug:
                self.log.debug('Receive [{0}]:\n{1}'.format(body['action'], ujson.dumps(result)))

            if 'error' in result:
                raise NanioException(result['error'], status)

        except ClientConnectionError as err:
            self.log.critical('Error connecting to backend: {0}'.format(err))
            raise NanioException('Backend connection error', 500)
        except HttpProcessingError as err:
            self.log.warning('{0} (action: {1}) '.format(err.message, body['action']))
            raise NanioException(err.message, err.code)

        return status, result
