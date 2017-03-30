#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from db.providers.archive_provider import ArchiveProvider
from db.database import pg_vacuum
import setproctitle

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

async def news_observer(progress=False):
    sem = asyncio.Semaphore(settings.LIMIT)
    kwargslist = (
        {
            'url': url.strip(),
            'include_text': keyword_builder(keywords),
            'ap': ap,
            'name': name
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
        print("[{}] {}".format(data['source'], data['info']))
        if __debug__:
            if 'supplements' == data['source'] and 'items' in data:
                print("→({}){}".format(data['url'], data['items']))

    db_url = settings.DATABASE_URL
    pg_vacuum(db_url.startswith('postgres://'))

    loop.close()
