# -*- coding: utf-8 -*-

import aiohttp
import functools
import ujson

from os import environ
from logging import LoggerAdapter
from aiohttp.client_exceptions import ClientConnectionError
from aiohttp.http_exceptions import HttpProcessingError
from marshmallow import ValidationError
from sanic import response, views

from nanio.exceptions import NanioException
from nanio.handlers._common import http_post
from nanio.schemas import ACTIONS_SCHEMAS
from nanio.log import Log


def inject_log_meta(func):
    def inner(self, request, *args, **kwargs):
        self.log = LoggerAdapter(self.log, {'host': request.ip})
        return func(self, request, *args, **kwargs)

    return inner


class NodeRPCProxyView(views.HTTPMethodView):
    log = Log.node_rpc

    def __init__(self, cfg):
        self._action = None
        self._cfg = cfg
        self._debug = cfg.core['debug']

    async def _rpc_request(self, address, payload):
        """Performs an RPC request

        :param payload: payload to pass along to the Node RPC server
        :return: (status code, JSON response)
        """

        if self._debug:
            self.log.debug('Send [{0}]:\n{1}'.format(self._action, payload))
        else:
            self.log.info('Send [{0}]'.format(self._action))

        async with aiohttp.ClientSession() as client:
            return await http_post(client, 'http://{0}'.format(address), payload)

    async def _get_validated_payload(self, request):
        """Deserialize and validate JSON payload

        :return: Validated JSON body
        """

        payload = request.json

        if not payload or 'action' not in payload:
            raise NanioException('Missing action in payload', 400)

        self._action = payload['action']
        schema = ACTIONS_SCHEMAS.get(self._action, None)

        if not schema:
            raise NanioException('Unknown action', 422)
        elif self._action not in self._cfg.rpc['actions_public']:
            raise NanioException('Disallowed action', 422)
        elif self._action in self._cfg.rpc['actions_protected']:
            pass

        try:
            validated = schema.load(payload).data
        except ValidationError as err:
            get_errors = functools.partial(ujson.dumps, err.messages)

            if self._debug:
                self.log.debug('Validation failed:\n{0}'.format(get_errors(indent=4)))
            else:
                pass
                # logger.warning('Payload validation failed (action: {0})'.format(self._action))

            raise NanioException(get_errors(), 422)

        return schema.dumps(validated).data

    @inject_log_meta
    async def post(self, request):
        if not self._cfg.rpc['enabled']:
            return response.json({'result': 'RPC proxy disabled'}, 200)

        payload = await self._get_validated_payload(request)

        try:
            status, result = await self._rpc_request(request.app.node_url, payload)
            if self._debug:
                self.log.debug('Receive [{0}]:\n{1}'.format(self._action, ujson.dumps(result)))

            if 'error' in result:
                raise NanioException(result['error'], status)

        except ClientConnectionError as err:
            self.log.critical('Error connecting to backend: {0}'.format(err))
            raise NanioException('Backend connection error', 500)
        except HttpProcessingError as err:
            self.log.warning('{0} (action: {1}) '.format(err.message, self._action))
            raise NanioException(err.message, err.code)

        return response.json(result, status)
