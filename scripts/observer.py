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
import requests
import configparser
from db.providers.archive_provider import ArchiveProvider


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
limit = 5

ap = ArchiveProvider()

async def news_observer():
    sem = asyncio.Semaphore(limit)
    kwargslist = (
        {
            'url': url.strip(),
            'include_text': keyword_builder(keywords),
            'ap': ap,
            'name': name
        } for name, url in feeds
    )
    result = await run_all_async(archive_feed_by_filter, kwargslist, sem, True)
    return (item for item in result if item)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    print("[Link Start]")
    loop = asyncio.get_event_loop()
    items = loop.run_until_complete(news_observer())

    for item in items:
        print("[{}] {}".format(item['source'], item['info']))

    loop.close()
