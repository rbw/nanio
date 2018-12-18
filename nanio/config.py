# -*- coding: utf-8 -*-

import re
from os import environ as env
from nanio.schemas import CoreSettings, RPCSettings, get_rpc_schemas
from nanio.utils import yaml_parse


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
RPC_ADDRESSES = to_list(env.get('RPC_NODES')) or yml_rpc['nodes']
RPC_PATH = env.get('RPC_PATH') or yml_rpc['path']

actions_public = to_list(env.get('RPC_ACTIONS_PUBLIC')) or yml_rpc['actions_public']
actions_protected = to_list(env.get('RPC_ACTIONS_PROTECTED')) or yml_rpc['actions_protected']

RPC_SCHEMAS = get_rpc_schemas(actions_public, actions_protected)

# Override Sanic defaults
LOGO = False
REQUEST_MAX_SIZE = 1000000

# MongoDB settings
"""MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME", "user")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", "password")
MONGODB_HOST = os.environ.get("MONGODB_HOST", "mongodb")
MONGODB_PORT = to_int(os.environ.get("MONGODB_PORT", 27017))
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "")
MONGODB_URI = 'mongodb://{}:{}@{}:{}/{}'.format(
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
    MONGODB_HOST,
    MONGODB_PORT,
    MONGODB_DATABASE
)
"""
