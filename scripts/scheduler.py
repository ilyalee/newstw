#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import settings
import asyncio
from observer import news_observer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    executors = {
        'default': ThreadPoolExecutor(settings.LIMIT),
        'processpool': ProcessPoolExecutor(os.cpu_count())
    }
    scheduler = AsyncIOScheduler(executors=executors)
    # every hours
    scheduler.add_job(news_observer, 'cron', minute=0, timezone="Asia/Taipei")
    scheduler.start()
    print("News Observer started.")
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    asyncio.get_event_loop().run_forever()
