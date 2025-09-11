#!/usr/bin/env python3

"""
An asynchronous coroutine that takes
in an integer argument with a default
value of 10.It waits for a random delay
between 0 and max_delay and eventually
returns the  max_delay.
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Wait for the max_delay and return the max_delay"""

    delay = max_delay * random.random()
    await asyncio.sleep(delay)
    return delay
