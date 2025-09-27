#!/usr/bin/env python3

"""
Create a measure_time function with integers
n and max_delay as arguments that measures the
total execution time for wait_n(n, max_delay),
and returns total_time / n.Your function should
return a float. Use the time module to measure
an approximate elapsed time.
"""

from time import time
from asyncio import run

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ Return execution time for wait_n given
    `n` and `max_delay`. """
    time_0 = time()
    run(wait_n(n, max_delay))
    time_1 = time()
    elapsed_time = time_1 - time_0
    return elapsed_time / n
