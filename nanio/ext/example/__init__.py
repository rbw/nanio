# -*- coding: utf-8 -*-

from .controller import ExampleController
from .service import ExampleService
from .documents import Example
from nanio.ext import Extension

EXAMPLE = Extension(
    name='example',
    controllers=[ExampleController],
    service=ExampleService(),
    documents=[Example]
)
