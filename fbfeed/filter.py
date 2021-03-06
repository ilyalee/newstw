#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbfeed.utils.fbfeed_utils import fb_init, load_obj, load_pages, load_fb_source
from utils.data_utils import fb_time_to_local, data_filter, data_inserter, data_cleaner, data_hasher, data_updater, dict_blocker, dict_renamer, data_remover
import settings
from utils.async_utils import as_run


class FbFeedFilter:

    def __init__(self, fbid, num=20, include_text='', search=False):
        self.fbid = fbid
        self.include_text = include_text
        self.search = search
        self.num = int(num)
        self.graph = fb_init()
        self.tzinfo = settings.TIMEZONE
        self.fields = ["id", "message", "created_time", "from", "permalink_url"]

    def _download(self, encoding='utf-8'):
        items = []
        fields = ",".join(self.fields)
        obj = load_obj(self.graph, self.fbid, search=self.search)
        if obj:
            items = load_pages(self.graph, self.fbid, "feed", self.num,
                               search=self.search, date_format="U", fields=fields)
        return items

    def _data_prepare(self, items):
        items = fb_time_to_local("created_time", self.tzinfo, items)
        items = data_remover(None, "message", items)
        return items

    def _data_filter(self, items):
        items = data_filter(self.include_text, ["message", "story"], items)
        return items

    def _data_produce(self, items):
        items = data_cleaner("message", items)
        items = data_cleaner("story", items)
        items = data_inserter(self.include_text, "keyword", items)
        items = dict_renamer("fbid", "id", items)
        items = dict_renamer("link", "permalink_url", items)
        items = dict_renamer("published", "created_time", items)
        items = data_hasher("hash", ["fbid", "published"], items)
        items = data_updater("from_id", "from", lambda x: x["id"], True, items)
        items = data_updater("from_name", "from", lambda x: x["name"], True, items)
        items = dict_blocker(["from"], items)
        items = data_inserter(self.fbid, "source", items)
        return items

    def output(self):
        items = self._download()
        items = self._data_prepare(items)
        items = self._data_filter(items)
        items = self._data_produce(items)
        return items

    async def as_output(self):
        items = await as_run(mode='process')(self._download)()
        items = await as_run(mode='process')(self._data_prepare)(items)
        items = await as_run(mode='process')(self._data_filter)(items)
        items = await as_run(mode='process')(self._data_produce)(items)
        return items
