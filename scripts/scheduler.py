#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from archiver.controllers.newsfeed import archive_feed_by_filter
from utils.data_utils import keyword_builder
import asyncio
import configparser
config = configparser.ConfigParser()
config.read('config/feeds.cfg')
sources_pm = config.items("Print media")
sources_em = config.items("Electronic media")
keywords = config.get("Feed filter", "keywords")

async def news_observer():
    print("[Link Start]")
    include_text = keyword_builder(keywords)
    all_tasks = asyncio.gather(*[archive_feed_by_filter(url, include_text) for name, url in sources_pm], *[archive_feed_by_filter(url, include_text) for name, url in sources_em], loop=asyncio.get_event_loop())

    await all_tasks

    print("[All Done]")

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    # every hours
    scheduler.add_job(news_observer, 'cron', minute=0, timezone="Asia/Taipei")

    scheduler.start()
    print("News Observer started.")
    #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
