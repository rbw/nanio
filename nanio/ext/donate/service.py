# -*- coding: utf-8 -*-

from nanio.ext import BaseService


class DonateService(BaseService):
    def __init__(self):
        self.node = self.ext['node'].svc

    def send(self):
        # print(self.node)
        print('hej')
