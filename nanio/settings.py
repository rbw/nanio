# -*- coding: utf-8 -*-

import re
import yaml

from os import environ as env
from nanio.schemas import SettingsCore, SettingsRPC


def yaml_parse(_dir, file):
    path = '{0}/{1}'.format(_dir, file)
    with open(path, 'r') as stream:
        return yaml.load(stream)


def settings_from_yaml(*args):
    _dir = env.get('SETTINGS_DIR', 'settings')
    return yaml_parse(_dir, *args)


# Parse settings from YAML files, then load it with Marshmallow for validation and defaults.
yml_core = SettingsCore().load(settings_from_yaml('core.yml')).data
yml_rpc = SettingsRPC().load(settings_from_yaml('rpc.yml')).data

# Create configuration as expected by Sanic, prefer environment over file.
APP_HOST = env.get('APP_HOST') or yml_core['listen_host']
APP_PORT = to_int(env.get('APP_HOST')) or yml_core['listen_port']
APP_DEBUG = to_bool(env.get('APP_DEBUG')) or yml_core['debug']
APP_WORKERS = to_int(env.get('APP_WORKERS')) or yml_core['workers']

# MongoDB
MONGODB_HOST = env.get('MONGODB_HOST') or yml_core['mongodb_host']
MONGODB_PORT = env.get('MONGODB_PORT') or yml_core['mongodb_port']

# Set up RPC
RPC_ENABLED = to_bool(env.get('RPC_ENABLED')) or yml_rpc['enabled']
RPC_NODES = to_list(env.get('RPC_NODES')) or yml_rpc['nodes']

RPC_COMMANDS_PUBLIC = to_list(env.get('RPC_COMMANDS_PUBLIC')) or yml_rpc['commands']['public']
RPC_COMMANDS_PROTECTED = to_list(env.get('RPC_COMMANDS_PROTECTED')) or yml_rpc['commands']['protected']
RPC_COMMANDS_PRIVATE = to_list(env.get('RPC_COMMANDS_PRIVATE')) or yml_rpc['commands']['private']

# Override Sanic defaults
LOGO = None
REQUEST_MAX_SIZE = 1000000
REQUEST_TIMEOUT = 60
