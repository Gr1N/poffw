# -*- coding: utf-8 -*-

import json
from http import HTTPStatus

from aiohttp import web

from helpers import complexity, hashcash, random_string

__all__ = (
    'login_task',
    'login',
)


X_POFFW_HEADER = 'X-POFFW'
X_POFFW_EXPIRE = 60


async def login_task(request):
    redis = request.app['redis']

    user_ip, _ = request.transport.get_extra_info('peername')

    token = random_string()
    bits = await complexity.get(redis, user_ip)
    task = hashcash.new(bits=bits)

    await redis.set(token, json.dumps(task))
    await redis.expire(token, X_POFFW_EXPIRE)

    return web.json_response(data=task, headers={
        X_POFFW_HEADER: token,
    })


async def login(request):
    data = await request.json()

    counter = data.get('counter')
    login = data.get('login')
    password = data.get('password')

    token = request.headers.get(X_POFFW_HEADER)
    if not all((token, counter, login, password,)):
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    redis = request.app['redis']

    task = await redis.get(token)
    if not task:
        return web.Response(status=HTTPStatus.BAD_REQUEST)

    await redis.delete(token)

    task = json.loads(task.decode('utf-8'))
    task['counter'] = counter
    if not hashcash.verify(**task):
        user_ip, _ = request.transport.get_extra_info('peername')
        await complexity.store(redis, user_ip)

        return web.Response(status=HTTPStatus.BAD_REQUEST)

    return web.json_response()
