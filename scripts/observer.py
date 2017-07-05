#!/usr/bin/env python
# -*- coding: utf-8 -*-

import better_exceptions
import os
import sys
sys.path.append(os.getcwd())

import asyncio
from archiver.controllers.newsfeed import archive_feed_by_filter
from utils.async_utils import run_all_async, sem_async, wait_with_progress
from utils.data_utils import keyword_builder
from itertools import chain, repeat
import settings
import configparser
from db.providers import ArchiveProvider
from db.providers import ObserverStatProvider
from db.utils.db_utils import auto_vacuum
import setproctitle
import gc

setproctitle.setproctitle(__name__)


def load_feeds(config, lst):
    collect = []
    for name in lst:
        sources = config.items(name)
        feeds = list(chain.from_iterable(zip(repeat(name), urls.split(","))
                                         for name, urls in sources))
        collect = collect + feeds
    return collect

config = configparser.ConfigParser()
config.read('config/feeds.cfg')

feeds = load_feeds(config, ['Print media', 'Electronic media'])
keywords = config.get("Feed filter", "keywords")

ap = ArchiveProvider()
osp = ObserverStatProvider()

async def news_observer(progress=False):
    sem = asyncio.Semaphore(settings.LIMIT)
    kwargslist = (
        {
            'url': url.strip(),
            'include_text': keyword_builder(keywords),
            'ap': ap,
            'connections': settings.CONNECTIONS_PER_FEED
        } for name, url in feeds
    )
    return await run_all_async(archive_feed_by_filter, kwargslist, sem, progress)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print("[Link Start]")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(news_observer(progress=True))

    for data in result:
        if 'count' in data:
            osp.save(data)
        print("[{}] {}".format(data['source'], data['info']))
        if __debug__:
            if 'supplements' == data['source'] and 'items' in data:
                print("→({}){}".format(data['url'], data['items']))

    result = None
    gc.collect()

    auto_vacuum()

    loop.close()
