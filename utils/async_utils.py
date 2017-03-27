import asyncio
import os
import tqdm
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


async def wait_with_progress(coros):
    return [await f for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros))]


def as_run(loop=None, count=None, mode=None):
    def _(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            loop = kwargs.get('loop', asyncio.get_event_loop())
            count = kwargs.get('count', os.cpu_count())
            mode = kwargs.get('mode', 'thread')
            pool = lambda mode, count: ProcessPoolExecutor(
                count) if mode == 'process' else ThreadPoolExecutor(count)
            return asyncio.ensure_future(loop.run_in_executor(pool(mode, count), partial(func, *args, **kwargs)))
        return wrapper
    return _


async def run_all_async(func, kwargslist=None, sem=None, progress=False):
    if not progress:
        return await asyncio.gather(*[asyncio.ensure_future(sem_async(func, sem, **kwargs)) for kwargs in kwargslist])
    else:
        return await wait_with_progress([sem_async(func, sem, **kwargs) for kwargs in kwargslist])


async def sem_async(func, sem, *args, **kwargs):
    with await sem:
        return await func(*args, **kwargs)
