# -*- coding: utf-8 -*-

import aiohttp_jinja2

__all__ = (
    'index',
)


@aiohttp_jinja2.template('index.jinja2')
def index(request):
    return {}
