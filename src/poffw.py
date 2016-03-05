# -*- coding: utf-8 -*-

import asyncio

import aiohttp_jinja2
import aioredis
import jinja2
from aiohttp import web

import handlers


async def get_app():
    redis = await aioredis.create_redis(('localhost', 6379,), db=1)

    app = web.Application()
    app['redis'] = redis

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))

    app.router.add_route('GET', '/', handlers.index)
    app.router.add_route('GET', '/login', handlers.login_task)
    app.router.add_route('POST', '/login', handlers.login)

    async def close_redis(app):
        app['redis'].close()

    app.on_shutdown.append(close_redis)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())
    web.run_app(app)
