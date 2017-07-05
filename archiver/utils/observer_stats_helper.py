#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.providers import ObserverStatProvider


class ObserverStatHelper():

    def __init__(self, ap):
        self.ap = ap

    def fetch_observer(self, page, limit):
        return self.ap.load_observer_by_page(page, limit)

    async def as_fetch_observer(self, page, limit):
        return await self.ap.as_load_observer_by_page(page, limit)

    def fetch_observer_count(self):
        return self.ap.sum()

    async def as_fetch_observer_count(self):
        return await self.ap.as_sum()

    def fetch_observer_today_count(self):
        return self.ap.sum_observer_today()

    async def as_fetch_observer_today_count(self):
        return await self.ap.as_sum_observer_today()

    def fetch_observer_yesterday_count(self):
        return self.ap.sum_observer_yesterday()

    async def as_fetch_observer_yesterday_count(self):
        return await self.ap.as_sum_observer_yesterday()

    def fetch_observer_month_count(self):
        return self.ap.sum_observer_month()

    async def as_fetch_observer_month_count(self):
        return await self.ap.as_sum_observer_month()


osh = ObserverStatHelper(ObserverStatProvider())
