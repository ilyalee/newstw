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
    return await news_observer_v2()

async def news_observer_v1():
    sem = asyncio.Semaphore(limit)
    return await wait_with_progress([sem_async(archive_feed_by_filter, sem, url.strip(), keyword_builder(keywords), ap, name) for name, url in feeds])


async def news_observer_v2():
    sem = asyncio.Semaphore(limit)
    arglist = [
        {
            'url': url.strip(),
            'include_text': keyword_builder(keywords),
            'ap': ap,
            'name': name
        } for name, url in feeds
    ]
    return await run_all_async(archive_feed_by_filter, arglist, sem, True)


if __name__ == '__main__':
    print("[Link Start]")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(news_observer())
    for data in result:
        print("[{}] {}".format(data['source'], data['info']))
    loop.close()
    sys.exit(0)
