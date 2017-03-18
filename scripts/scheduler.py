#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BlockingScheduler


#TODO: add real jobs
def run():
    print('Tick! The time is: %s' % datetime.now())

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(run, 'interval', hours=1)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
