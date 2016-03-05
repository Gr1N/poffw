# -*- coding: utf-8 -*-

"""
stamp format: ver:bits:date:resource:[ext]:rand:counter
docs: http://www.hashcash.org/docs/hashcash.html#stamp_format__version_1_
"""

import sys
import time

import sha3

from helpers import random_string

__all__ = (
    'new',
    'solve',
    'verify',
)


def new(bits=1):
    return {
        'ver': 1,
        'bits': bits,
        'date': int(time.time()),
        'resource': 'poffw',
        'ext': '',
        'rand': random_string(),
    }


def solve(**kwargs):
    kwargs = kwargs.copy()

    for counter in range(1, sys.maxsize):
        kwargs['counter'] = counter
        if not verify(**kwargs):
            continue

        return counter

    return None


def verify(**kwargs):
    stamp = '{ver}:{bits}:{date}:{resource}:{ext}:{rand}:{counter}'.format(**kwargs)
    stamp = stamp.encode('utf-8')
    prefix = '0' * kwargs['bits']

    return sha3.sha3_512(stamp).hexdigest().startswith(prefix)
