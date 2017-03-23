import asyncio
import os
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

'''
https://www.pythonsheets.com/notes/python-concurrency.html
'''


def profile(func, note=None):
    async def wrapper(*args, **kwargs):
        import time
        start = time.time()
        if asyncio.iscoroutine(func):
            result = func(*args, **kwargs)
        else:
            result = await func(*args, **kwargs)
        end = time.time()
        if note:
            print(func.__name__, end - start, 's')
        else:
            print(end - start)
        return result
    return wrapper


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


@profile
async def run_all_async(func, partials=None, loop=None, count=None, mode='thread', timeout=120, limit=5):
    collect = []
    sem = asyncio.Semaphore(limit)
    if not loop:
        loop = asyncio.get_event_loop()
    if not count:
        count = os.cpu_count()
    for partial in partials:
        async with sem:
            collect.append(await(func)(**partial))

    return collect
