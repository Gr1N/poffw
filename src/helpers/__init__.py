# -*- coding: utf-8 -*-

import random
import string

random = random.SystemRandom()

__all__ = (
    'random_string',
)


def random_string():
    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(16)
    )
