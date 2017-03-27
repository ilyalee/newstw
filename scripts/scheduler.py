#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
from observer import news_observer
from apscheduler.schedulers.asyncio import AsyncIOScheduler

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    scheduler = AsyncIOScheduler()
    executors = {
        'default': ThreadPoolExecutor(5),
        'processpool': ProcessPoolExecutor(os.cpu_count())
    }
    # every hours
    scheduler.add_job(news_observer, 'cron', minute=0, timezone="Asia/Taipei", executors=executors)
    scheduler.start()
    print("News Observer started.")
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    asyncio.get_event_loop().run_forever()
