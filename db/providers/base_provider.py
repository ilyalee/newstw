#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db.database import scoped_session, query_session, Session
from db.utils.db_utils import load_as_objs, decode_hashid
from sqlalchemy import exc, desc


class BaseProvider():

    def __init__(self, cls):
        self.cls = cls

    def reload(self, items):
        return load_as_objs(self.cls, items)

    @decode_hashid
    def load(self, id):
        if not id or not isinstance(id, int):
            return ""
        with query_session() as session:
            result = session.query(self.cls).get(id)
            item = result.to_dict()
        return item

    def find_all(self, orderby):
        items = []
        if not orderby:
            return items
        with query_session() as session:
            result_set = session.query(self.cls).order_by(desc(getattr(self.cls, orderby))).all()
            items = [item.to_dict() for item in result_set]
        return items

    def find_items_by_datetime_between(self, name, start, end):
        items = []
        if not name:
            return items
        with query_session() as session:
            result_set = session.query(self.cls).filter(getattr(self.cls, name).between(
                start, end)).order_by(desc(getattr(self.cls, name))).all()
            items = [item.to_dict() for item in result_set]
        return items

    def find_distinct_items_by(self, name, items):
        if not name or not items:
            return items
        with query_session() as session:
            existed = [item[name] for item in items]
            result_set = session.query(self.cls).filter(getattr(self.cls, name).in_(existed)).all()
            dups = [dup.to_dict() for dup in result_set]
            items = [item for item in items if item[name] not in dups]
        return items

    def save_all(self, items):
        objs = self.reload(items)
        acceptances = len(objs)
        with scoped_session() as session:
            for obj in objs:
                try:
                    with session.begin_nested():
                        session.add(obj)
                except exc.IntegrityError:
                    acceptances = acceptances - 1
        return acceptances
