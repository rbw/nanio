# -*- coding: utf-8 -*-

import yaml


def yaml_parse(_dir, file):
    path = '{0}/{1}'.format(_dir, file)
    with open(path, 'r') as stream:
        return yaml.load(stream)

