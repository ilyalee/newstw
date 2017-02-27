#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs
from sqlalchemy import exc

class BaseProvider():

    def __init__(self, cls):
        self.cls = cls

    def load(self, items):
        return load_as_objs(self.cls, items)

    def find_distinct_items_by(self, name, existed, items):
        with query_session() as session:
            result_set = session.query(self.cls).filter(getattr(self.cls, name).in_(existed)).all()
            dups = [dup.__dict__[name] for dup in result_set]
            items = [item for item in items if item[name] not in dups]
        return items

    def save_all(self, items):
        objs = self.load(items)
        acceptances = len(objs)
        with scoped_session() as session:
            for obj in objs:
                try:
                    with session.begin_nested():
                        session.add(obj)
                except exc.IntegrityError:
                    acceptances = acceptances - 1
        return acceptances
