# -*- coding: utf-8 -*-

import yaml
from yaml.parser import ParserError as YAMLParseError
from logging import LoggerAdapter


async def http_post(session, url, payload):
    async with session.post(url, data=payload) as result:
        return await result.json()


def yaml_parse(_dir, file):
    path = '{0}/{1}'.format(_dir, file)
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except YAMLParseError as err:
            # @TODO - handle properly
            print(str(err))
            raise


def inject_log_meta(func):
    def inner(self, request, *args, **kwargs):
        self.log = LoggerAdapter(self.log, {'host': request.ip})
        return func(self, request, *args, **kwargs)

    return inner
