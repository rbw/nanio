# -*- coding: utf-8 -*-

import re
import yaml

from os import environ as env
from nanio.schemas import CoreSettings, RPCSettings


def yaml_parse(_dir, file):
    path = '{0}/{1}'.format(_dir, file)
    with open(path, 'r') as stream:
        return yaml.load(stream)


def settings_from_yaml(*args):
    _dir = env.get('SETTINGS_DIR', 'settings')
    return yaml_parse(_dir, *args)


def to_bool(value):
    return str(value).strip().lower() in ['1', 'true', 'yes']


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def to_list(value):
    """Allow comma and whitespace separation"""
    if not isinstance(value, str):
        return False

    return list(filter(None, re.split(r'[,| ]', value)))


# Parse settings from YAML files, then load it with Marshmallow for validation and defaults.
yml_core = CoreSettings(strict=True).load(settings_from_yaml('core.yml')).data
yml_rpc = RPCSettings(strict=True).load(settings_from_yaml('rpc.yml')).data

# Create configuration as expected by Sanic, prefer environment over file.
APP_HOST = env.get('APP_HOST') or yml_core['host']
APP_PORT = to_int(env.get('APP_HOST')) or yml_core['port']
APP_DEBUG = to_bool(env.get('APP_DEBUG')) or yml_core['debug']
APP_WORKERS = to_int(env.get('APP_WORKERS')) or yml_core['workers']

# Set up RPC
RPC_ENABLED = to_bool(env.get('RPC_ENABLED')) or yml_rpc['enabled']
RPC_NODES = to_list(env.get('RPC_NODES')) or yml_rpc['nodes']
RPC_PATH = env.get('RPC_PATH') or yml_rpc['path']

RPC_ACTIONS_PUBLIC = to_list(env.get('RPC_ACTIONS_PUBLIC')) or yml_rpc['actions_public']
RPC_ACTIONS_PROTECTED = to_list(env.get('RPC_ACTIONS_PROTECTED')) or yml_rpc['actions_protected']

# Override Sanic defaults
LOGO = None
REQUEST_MAX_SIZE = 1000000

# MongoDB
MONGODB_HOST = env.get('MONGODB_HOST') or yml_core['mongodb_host']
