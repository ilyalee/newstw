#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db.database import scoped_session, query_session, Session
from db.models.archives import Archive
from sqlalchemy import exc
from db.providers.base_provider import BaseProvider


class ArchiveProvider(BaseProvider):

    def __init__(self):
        super().__init__(Archive)
