import asyncio
import os
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def as_run(loop=None, count=None, mode='thread'):
    def _(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            loop = kwargs.get('loop', asyncio.get_event_loop())
            count = kwargs.get('count', os.cpu_count())
            if mode == 'thread':
                executor = ThreadPoolExecutor(count)
            elif mode == 'process':
                executor = ProcessPoolExecutor(count)
            future = loop.run_in_executor(executor, partial(func, *args, **kwargs))
            return asyncio.ensure_future(future)
        return wrapper
    return _


async def run_all_async(func, arglist=None, sem=None):
    done, _ = await asyncio.wait([sem_async(func, sem, **kwargs) for kwargs in arglist])
    return done


async def sem_async(func, sem, *args, **kwargs):
    with await sem:
        return await func(*args, **kwargs)
