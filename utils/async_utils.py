import asyncio
import os
import functools
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def as_run(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(os.cpu_count())
    future = loop.run_in_executor(executor, functools.partial(func, *args, **kwargs))
    return asyncio.ensure_future(future)


def as_run_pro(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(os.cpu_count())
    future = loop.run_in_executor(executor, functools.partial(func, *args, **kwargs))
    return asyncio.ensure_future(future)
