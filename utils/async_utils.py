import asyncio
import os
from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

'''
https://www.pythonsheets.com/notes/python-concurrency.html
'''


def profile(func, note):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(note, end - start)
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
