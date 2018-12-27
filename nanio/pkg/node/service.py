# -*- coding: utf-8 -*-

import functools
import ujson

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.http_exceptions import HttpProcessingError
from marshmallow import ValidationError
from jetfactory.base import JetfactoryService

from nanio.exceptions import NanioException
from nanio.settings import RPC_NODES, RPC_COMMANDS_PUBLIC, RPC_COMMANDS_PROTECTED, RPC_COMMANDS_PRIVATE


from .schemas import COMMANDS_SCHEMAS


class Schemas:
    def __init__(self):
        self.by_action = {s.Meta.action: s for s in COMMANDS_SCHEMAS}
        self.by_category = self.__get_by_category()

    def __get_by_category(self):
        groups = {}

        for _, schema in sorted(self.by_action.items()):
            group = schema.Meta.group
            action = schema.Meta.action

            if action in RPC_COMMANDS_PROTECTED:
                access = 'protected'
            elif action in RPC_COMMANDS_PRIVATE:
                access = 'private'
            else:
                access = 'public'

            action = {
                'name': schema.Meta.name,
                'action': action,
                'description': schema.Meta.description,
                'enabled': action in RPC_COMMANDS_PUBLIC + RPC_COMMANDS_PROTECTED + RPC_COMMANDS_PRIVATE,
                'access': access,
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


class NodeService(JetfactoryService):
    def __init__(self, *args, **kwargs):
        super(NodeService, self).__init__(*args, **kwargs)
        self.node_url = 'http://' + RPC_NODES[0]
        self.schemas = Schemas()

    async def node_rpc_request(self, payload):
        return await self.http_post(self.node_url, payload)

    async def validate_command(self, body, is_internal):
        if not body or 'action' not in body:
            raise NanioException('Missing action in payload', 400)

        action = body['action']
        schema = self.schemas.by_action.get(action, None)

        if not schema:
            raise NanioException('Unknown command', 404)
        elif is_internal:
            pass
        elif action in RPC_COMMANDS_PRIVATE:
            raise NanioException('Forbidden', 403)
        elif action in RPC_COMMANDS_PROTECTED and True:  # TODO: check auth
            raise NanioException('Unauthorized', 401)

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

    async def send(self, body, is_internal=True):
        command = await self.validate_command(body, is_internal)

        if self.debug:
            self.log.debug('Command relay [{0}]:\n{1}'.format(body['action'], command))
        else:
            self.log.info('Command relay [{0}]'.format(body['action']))

        try:
            result, status = await self.http_post(self.node_url, command)

            if self.debug:
                self.log.debug('Relay response [{0}]:\n{1}'.format(body['action'], result))

            if 'error' in result:
                raise NanioException(result['error'], status)

        except ClientConnectionError as err:
            self.log.critical('Error connecting to backend: {0}'.format(err))
            raise NanioException('Backend connection error', 500)
        except HttpProcessingError as err:
            self.log.warning('{0} (action: {1}) '.format(err.message, body['action']))
            raise NanioException(err.message, err.code)

        return result, status
