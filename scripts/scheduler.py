#!/usr/bin/env python
# -*- coding: utf-8 -*-

import better_exceptions
import os
import sys
sys.path.append(os.getcwd())

import settings
import asyncio
from observer import news_observer
from observer_facebook import facebook_observer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import setproctitle

setproctitle.setproctitle(__name__)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    scheduler = AsyncIOScheduler()
    # every hours
    scheduler.add_job(news_observer, 'cron', minute=0, timezone="Asia/Taipei")
    scheduler.add_job(facebook_observer, 'cron', minute=30, timezone="Asia/Taipei")
    scheduler.start()
    print("News Observer started.")
    # scheduler.print_jobs()
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    asyncio.get_event_loop().run_forever()
