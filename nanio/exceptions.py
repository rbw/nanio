# -*- coding: utf-8 -*-

from sanic.exceptions import SanicException


class NanioException(SanicException):
    def __init__(self, *args, **kwargs):
        self.log_message = kwargs.pop('write_log', False)

        super(NanioException, self).__init__(*args, **kwargs)
