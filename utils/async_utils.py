import asyncio
import os
import tqdm
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


async def wait_with_progress(coros):
    return [await f for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros))]


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


async def run_all_async(func, arglist=None, sem=None, progress=False):
    if not progress:
        return [await sem_async(func, sem, **kwargs) for kwargs in arglist]
    else:
        return await wait_with_progress([sem_async(func, sem, **kwargs) for kwargs in arglist])


async def sem_async(func, sem, *args, **kwargs):
    with await sem:
        return await func(*args, **kwargs)
