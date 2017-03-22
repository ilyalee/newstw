#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import asyncio
from archiver.controllers.newsfeed import archive_feed_by_filter
from utils.data_utils import keyword_builder
from itertools import chain, repeat
import asyncio
import configparser

config = configparser.ConfigParser()
config.read('config/feeds.cfg')
sources_pm = config.items("Print media")
sources_em = config.items("Electronic media")
urls_pm = list(chain.from_iterable(zip(repeat(name), urls.split(","))
                                   for name, urls in sources_pm))
urls_em = list(chain.from_iterable(zip(repeat(name), urls.split(","))
                                   for name, urls in sources_em))
urls_all = urls_pm + urls_em
keywords = config.get("Feed filter", "keywords")
timeout = 600
max_sem = 3

async def news_observer(loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    async def sem_run(sem, name, url, include_text):
        with await sem:
            return await archive_feed_by_filter(url, include_text)

    include_text = keyword_builder(keywords)
    sem = asyncio.Semaphore(max_sem)
    done, _ = await asyncio.wait([sem_run(sem, name, url.strip(), include_text) for name, url in urls_all], loop=loop, timeout=timeout)
    return done

if __name__ == '__main__':
    print("[Link Start]")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(news_observer(loop))
    for done in result:
        data = done.result()
        print("{}: {}".format(data['source'], data['info']))
    loop.close()
    sys.exit(0)
