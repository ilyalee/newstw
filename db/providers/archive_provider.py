#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc
from db.providers.base_provider import BaseProvider
import arrow

class ArchiveProvider(BaseProvider):

    def __init__(self):
        super().__init__(Archive)
        self.tzinfo = "Asia/Taipei"

    def load_report_all(self):
        return self.find_all(orderby="published")


    def load_report_today(self):
        start = arrow.now(self.tzinfo).floor('day').datetime
        end = arrow.now(self.tzinfo).ceil('day').datetime
        return self.find_items_by_datetime_between("published", start, end)
