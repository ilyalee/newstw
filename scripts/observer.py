#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import asyncio
from archiver.controllers.newsfeed import archive_feed_by_filter
from utils.async_utils import run_all_async
from utils.data_utils import keyword_builder
from itertools import chain, repeat
import requests
import configparser


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
timeout = 600
limit = 5


async def news_observer(loop=None):
    if not loop:
        loop = asyncio.get_event_loop()

    include_text = keyword_builder(keywords)
    return await run_all_async(archive_feed_by_filter, [
        {'url': url.strip(), 'include_text': include_text} for name, url in feeds], loop=loop, mode='process', timeout=timeout, limit=limit)

if __name__ == '__main__':
    print("[Link Start]")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(news_observer(loop))
    for data in result:
        if data:
            print("[{}] {}".format(data['source'], data['info']))
    loop.close()
    sys.exit(0)
