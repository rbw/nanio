# -*- coding: utf-8 -*-

import functools
import ujson

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.http_exceptions import HttpProcessingError
from marshmallow import ValidationError

from nanio.exceptions import NanioException
from nanio.config import RPC_NODES, RPC_ACTIONS_PUBLIC, RPC_ACTIONS_PROTECTED
from nanio.ext.base.service import NanioService

from .schemas import RPC_SCHEMAS
from .models import Test


class Schemas:
    def __init__(self):
        self.by_action = {s.Meta.action: s for s in RPC_SCHEMAS}
        self.by_category = self.__get_by_category()

    def __get_by_category(self):
        groups = {}

        for _, schema in sorted(self.by_action.items()):
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


class NodeService(NanioService):
    def __init__(self):
        self.node_url = 'http://' + RPC_NODES[0]
        self.schemas = Schemas()

    async def node_rpc_request(self, payload):
        return await self.http_post(self.node_url, payload)

    async def validate_body(self, body):
        if not body or 'action' not in body:
            raise NanioException('Missing action in payload', 400)

        action = body['action']
        schema = self.schemas.by_action.get(action, None)

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
        payload = await self.validate_body(body)

        if self.debug:
            self.log.debug('Send [{0}]:\n{1}'.format(body['action'], payload))
        else:
            self.log.info('Send [{0}]'.format(body['action']))

        try:
            result, status = await self.http_post(self.node_url, payload)

            if self.debug:
                self.log.debug('Receive [{0}]:\n{1}'.format(body['action'], result))

            if 'error' in result:
                raise NanioException(result['error'], status)

        except ClientConnectionError as err:
            self.log.critical('Error connecting to backend: {0}'.format(err))
            raise NanioException('Backend connection error', 500)
        except HttpProcessingError as err:
            self.log.warning('{0} (action: {1}) '.format(err.message, body['action']))
            raise NanioException(err.message, err.code)

        return result, status
