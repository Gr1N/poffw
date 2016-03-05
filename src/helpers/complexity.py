# -*- coding: utf-8 -*-

import time

__all__ = (
    'get',
    'store',
)


async def get(redis, user_ip):
    await store(redis, user_ip)

    attempts = await redis.mget(*keys(user_ip))
    attempts = sum(int(attempt) for attempt in attempts if attempt)

    # Just for tests, if want use something like this in your application
    # you should use configuration with predefined prairs (attempts, complexity)
    if attempts > 3:
        return 50

    return 1


async def store(redis, user_ip):
    k = key(user_ip)

    await redis.incr(k)
    await redis.expire(k, 120)  # two minutes


def keys(user_ip):
    end = int(time.time()) + 1
    start = end - 60  # one minute

    return [key(user_ip, sec=sec) for sec in range(start, end)]


def key(user_ip, sec=None):
    sec = sec or int(time.time())

    return '{user_ip}:{sec}'.format(user_ip=user_ip, sec=sec)
