# -*- coding: utf-8 -*-

import yaml
from logging import LoggerAdapter


async def http_post(session, url, payload):
    async with session.post(url, data=payload) as result:
        return await result.json()


def from_yaml(path):
    """yml => dict

    :param path: file path
    :return: contents
    """

    with open(path, 'r') as stream:
        return yaml.load(stream) or {}


def inject_log_meta(func):
    def inner(self, request, *args, **kwargs):
        self.log = LoggerAdapter(self.log, {'host': request.ip})
        return func(self, request, *args, **kwargs)

    return inner
