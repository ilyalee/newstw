#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from archiver.controllers.newsfeed import archive_feed_by_filter
from utils.data_utils import keyword_builder
from itertools import chain, repeat
import asyncio
import configparser
config = configparser.ConfigParser()
config.read('config/feeds.cfg')
sources_pm = config.items("Print media")
sources_em = config.items("Electronic media")
keywords = config.get("Feed filter", "keywords")

urls_pm = list(chain.from_iterable(zip(repeat(name), urls.split(","))
                                   for name, urls in sources_pm))
urls_em = list(chain.from_iterable(zip(repeat(name), urls.split(","))
                                   for name, urls in sources_em))

urls_all = urls_pm + urls_em
timeout = 420
max_sem = 5

async def news_observer():
    async def sem_run(sem, name, url, include_text):
        with await sem:
            print("{}: {}".format(name, url))
            return await archive_feed_by_filter(url, include_text)
    print("[Link Start]")
    include_text = keyword_builder(keywords)
    print("keywords: {}".format(include_text))
    sem = asyncio.Semaphore(max_sem)
    done, pending = await asyncio.wait([sem_run(sem, name, url.strip(), include_text) for name, url in urls_all], loop=asyncio.get_event_loop(), timeout=timeout)

    print("[All Done]")

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    # every hours
    scheduler.add_job(news_observer, 'cron', minute=0, timezone="Asia/Taipei")

    scheduler.start()
    print("News Observer started.")
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
