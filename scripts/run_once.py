#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from scheduler import news_observer

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(news_observer())
    loop.close()
