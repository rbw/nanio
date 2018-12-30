# -*- coding: utf-8 -*-

import functools
import ujson

from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.http_exceptions import HttpProcessingError
from marshmallow import ValidationError
from jetfactory.base import JetfactoryService
from jetfactory.exceptions import JetfactoryException

from .schemas import COMMANDS_SCHEMAS


class Schemas:
    def __init__(self, commands):
        self.commands = commands
        self.by_action = {s.Meta.action: s for s in COMMANDS_SCHEMAS}
        self.by_category = self.__get_by_category()

    def __get_by_category(self):
        groups = {}

        for _, schema in sorted(self.by_action.items()):
            group = schema.Meta.group
            action = schema.Meta.action

            if action in self.commands['protected']:
                access = 'protected'
            elif action in self.commands['private']:
                access = 'private'
            else:
                access = 'public'

            action = {
                'name': schema.Meta.name,
                'action': action,
                'description': schema.Meta.description,
                'enabled': action in self.commands['public'] + self.commands['protected'] + self.commands['private'],
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
    def __init__(self):
        self.node_url = 'http://' + self.cfg['nodes'][0]
        self.commands = self.cfg['commands']
        self.schemas = Schemas(self.commands)

    async def node_rpc_request(self, payload):
        return await self.http_post(self.node_url, payload)

    async def validate_command(self, body, is_internal):
        if not body or 'action' not in body:
            raise JetfactoryException('Missing action in payload', 400)

        action = body['action']
        schema = self.schemas.by_action.get(action, None)

        if not schema:
            raise JetfactoryException('Unknown command', 404)
        elif is_internal:
            pass
        elif action in self.commands['private']:
            raise JetfactoryException('Forbidden', 403)
        elif action in self.commands['protected'] and True:  # TODO: check auth
            raise JetfactoryException('Unauthorized', 401)

        try:
            validated = schema.load(body).data
        except ValidationError as err:
            get_errors = functools.partial(ujson.dumps, err.messages)

            if self.debug:
                self.log.debug('Validation failed:\n{0}'.format(get_errors(indent=4)))
            else:
                self.log.warning('Payload validation failed (action: {0})'.format(action))

            raise JetfactoryException(get_errors(), 422)

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
                raise JetfactoryException(result['error'], status)

        except ClientConnectionError as err:
            self.log.critical('Error connecting to backend: {0}'.format(err))
            raise JetfactoryException('Backend connection error', 500)
        except HttpProcessingError as err:
            self.log.warning('{0} (action: {1}) '.format(err.message, body['action']))
            raise JetfactoryException(err.message, err.code)

        return result, status
