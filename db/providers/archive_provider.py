#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc
from db.providers.base_provider import BaseProvider
import arrow
import settings
from utils.data_utils import dict_blocker, time_corrector

class ArchiveProvider(BaseProvider):

    def __init__(self):
        super().__init__(Archive)
        self.tzinfo = settings.TIMEZONE

    def load(self, id, blockers=[]):
        item = super().load(id)
        item = dict_blocker(blockers, item)
        item = time_corrector("published", item)
        item = time_corrector("updated", item)
        return item[0]

    def load_report_all(self):
        return self.find_all(orderby="published")

    def load_report_today(self):
        start = arrow.now(self.tzinfo).floor('day').datetime
        end = arrow.now(self.tzinfo).ceil('day').datetime
        return self.find_items_by_datetime_between("published", start, end)
