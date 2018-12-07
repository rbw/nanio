# -*- coding: utf-8 -*-

import yaml


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
