# -*- coding: utf-8 -*-

from jetfactory.exceptions import JetfactoryException


class NanioException(JetfactoryException):
    def __init__(self, *args, **kwargs):
        self.log_message = kwargs.pop('write_log', False)

        super(NanioException, self).__init__(*args, **kwargs)
