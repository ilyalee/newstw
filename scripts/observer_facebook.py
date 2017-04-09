#!/usr/bin/env python
# -*- coding: utf-8 -*-

import better_exceptions
import os
import sys
sys.path.append(os.getcwd())

import asyncio
from archiver.controllers.fbfeed import archive_feed_by_filter
from utils.async_utils import run_all_async, sem_async, wait_with_progress
from utils.data_utils import keyword_builder
from itertools import chain, repeat
import settings
import configparser
from db.providers import FacebookArchiveProvider
from db.utils.db_utils import auto_vacuum
import setproctitle

setproctitle.setproctitle(__name__)


config = configparser.ConfigParser()
config.read('config/fbfeeds.cfg')

feeds = config.items('Graph Objects')
keywords = config.get("Feed filter", "keywords")

ap = FacebookArchiveProvider()
async def facebook_observer(progress=False):
    sem = asyncio.Semaphore(settings.LIMIT)
    kwargslist = (
        {
            'fbid': fbid,
            'include_text': keyword_builder(keywords),
            'ap': ap,
            'num': 100
        } for fbid, name in feeds
    )
    return await run_all_async(archive_feed_by_filter, kwargslist, sem, progress)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print("[Link Start]")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(facebook_observer(progress=True))

    for data in result:
        print("[{}] {}".format(data['source'], data['info']))

    auto_vacuum()

    loop.close()
