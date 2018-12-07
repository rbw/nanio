# -*- coding: utf-8 -*-

import aiohttp
from sanic import response


async def handle_response(message, status, force_error=False):
    if force_error or status >= 300:
        message = {'error': message}
    else:
        message = {'result': message}

    return response.json(body=message, status=status)


async def get_request_action(request):
    return request.get('action', None)


async def http_post(client, url, payload):
    async with client.post(url, data=payload) as resp:
        result = await resp.json()
        return resp.status, result
